"""Publish only the explicitly versioned release artifacts using the CI-provided token.
No desktop credentials are read. Existing tags/assets are never deleted or retargeted.
"""
import os,json,urllib.request,urllib.error,urllib.parse,subprocess,hashlib,zipfile,io
REPO='patrickara1206/penaltyfeverpatrasedition'
PREVIOUS=[('v1.0.0','f826ad9fa6469b71395c54a4ff34c159929bd43e','Escudos, confrontos e primeira distribuição versionada.'),('v1.0.1','87f978c7286a9e349169636679ae7d206f49f26c','Arquivo histórico: identidade verde e dourada, uniformes e memória dos clubes. Contém falha no botão de iniciar temporada, corrigida na v1.0.3.'),('v1.0.2','ff890fa6260593645990fc9e5f29889d468c2581','Arquivo histórico: proteções de importação de saves, CSP e publicação gratuita. Contém falhas de início de temporada e comunicação do resultado com Ruffle, corrigidas na v1.0.3.'),('v1.0.3','40ef4c4ee1b7c387574c00b3def8cffacd3dc42c','Seleção de clubes em carrossel e correções de início e resultado das partidas.')]
def git(*args):return subprocess.check_output(['git',*args])
def request(method,path,payload=None,content_type='application/json',absolute=False):
 data=json.dumps(payload).encode()if isinstance(payload,dict)else payload
 url=path if absolute else 'https://api.github.com/repos/'+REPO+path
 if not url.startswith(('https://api.github.com/repos/'+REPO+'/','https://uploads.github.com/repos/'+REPO+'/')):raise ValueError('Unexpected destination')
 req=urllib.request.Request(url,data=data,method=method,headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json','Content-Type':content_type,'User-Agent':'PF-Versioned-Releases','X-GitHub-Api-Version':'2022-11-28'})
 try:
  with urllib.request.urlopen(req,timeout=180)as response:return json.load(response)
 except urllib.error.HTTPError as e:
  if e.code==404 and method=='GET':return None
  raise RuntimeError('GitHub release request failed: HTTP '+str(e.code))from None

def main():
 if os.environ.get('GITHUB_REPOSITORY')!=REPO or os.environ.get('GITHUB_REF')!='refs/heads/v1.0.4':raise RuntimeError('Unexpected repository/ref')
 latest=git('rev-parse','HEAD').decode().strip();rows=PREVIOUS+[('v1.0.4',latest,open('RELEASE-v1.0.4.md',encoding='utf-8-sig').read())]
 for tag,sha,notes in rows:
  blob=git('show',sha+':distribuicao/Penalty-Fever-2026-Edition.zip')
  with zipfile.ZipFile(io.BytesIO(blob))as z:
   if z.testzip()is not None:raise RuntimeError('Corrupt release archive: '+tag)
   if not any(n.endswith('/JOGAR.html')for n in z.namelist()):raise RuntimeError('Missing portable launcher')
  digest=hashlib.sha256(blob).hexdigest();filename='Penalty-Fever-2026-Edition-'+tag+'.zip'
  body=notes+'\n\nExtraia o ZIP inteiro e abra JOGAR.html em navegador moderno. Não requer instalação ou administrador. Consulte as limitações e créditos no pacote.\n\nSHA-256: `'+digest+'`\n'
  # Preserve any existing immutable release, and make a partial publication resumable.
  ref=request('GET','/git/ref/tags/'+tag)
  if ref and ref['object']['sha']!=sha:raise RuntimeError('Existing tag targets a different commit: '+tag)
  release=request('GET','/releases/tags/'+tag)
  if release is None:release=request('POST','/releases',{'tag_name':tag,'target_commitish':sha,'name':'Penalty Fever 2026 Edition · '+tag,'body':body,'draft':False,'prerelease':tag=='v1.0.4','make_latest':'true'if tag=='v1.0.3'else'false'})
  assets={a['name']:a for a in release.get('assets',[])}
  for name,data,mime in [(filename,blob,'application/zip'),('SHA256-'+tag+'.txt',(digest+'  '+filename+'\n').encode(),'text/plain')]:
   if name in assets:
    if assets[name]['size']!=len(data):raise RuntimeError('Existing asset differs; refusing overwrite: '+name)
    continue
   upload=release['upload_url'].split('{',1)[0]+'?name='+urllib.parse.quote(name)
   request('POST',upload,data,mime,absolute=True)
  print(tag,release['html_url'],filename,len(blob),digest)
if __name__=='__main__':main()
