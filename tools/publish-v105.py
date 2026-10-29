"""Publish only v1.0.5 through the repository's CI credential."""
import os,json,urllib.request,urllib.error,hashlib,subprocess,zipfile,io
REPO='patrickara1206/penaltyfeverpatrasedition';TAG='v1.0.5'
def request(method,path,data=None,mime='application/json'):
 url=path if path.startswith('https://uploads.github.com/repos/'+REPO+'/')else'https://api.github.com/repos/'+REPO+path
 body=json.dumps(data).encode()if isinstance(data,dict)else data
 req=urllib.request.Request(url,data=body,method=method,headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json','Content-Type':mime,'User-Agent':'PF-Releases'})
 try:
  with urllib.request.urlopen(req,timeout=180)as r:return json.load(r)
 except urllib.error.HTTPError as e:
  if e.code==404 and method=='GET':return None
  raise RuntimeError('GitHub request failed: HTTP '+str(e.code))from None
def main():
 if os.environ.get('GITHUB_REPOSITORY')!=REPO or os.environ.get('GITHUB_REF')!='refs/heads/'+TAG:raise RuntimeError('Unexpected repository/ref')
 sha=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip();blob=open('distribuicao/Penalty-Fever-2026-Edition.zip','rb').read();digest=hashlib.sha256(blob).hexdigest();name='Penalty-Fever-2026-Edition-'+TAG+'.zip'
 with zipfile.ZipFile(io.BytesIO(blob))as z:
  assert z.testzip()is None
  assert any(n.endswith('/app/settings.js')for n in z.namelist())
 ref=request('GET','/git/ref/tags/'+TAG)
 updated=bool(ref and ref['object']['sha']!=sha)
 if updated:name='Penalty-Fever-2026-Edition-'+TAG+'-'+sha[:7]+'.zip'
 release=request('GET','/releases/tags/'+TAG)
 if release is None:release=request('POST','/releases',{'tag_name':TAG,'target_commitish':sha,'name':'Penalty Fever 2026 Edition · '+TAG,'body':open('RELEASE-v1.0.5.md',encoding='utf-8-sig').read()+'\n\nSHA256: `'+digest+'`','draft':False,'prerelease':True,'make_latest':'false'})
 if updated:release=request('PATCH','/releases/'+str(release['id']),{'body':'**Pacote atualizado:** [baixar ZIP](https://github.com/'+REPO+'/releases/download/'+TAG+'/'+name+'). Código: '+sha+'. A tag e o arquivo originais foram preservados.\n\n'+open('RELEASE-v1.0.5.md',encoding='utf-8-sig').read()+'\n\nSHA256: `'+digest+'`'})
 existing={a['name']:a for a in release['assets']}
 for filename,data,mime in [(name,blob,'application/zip'),('SHA256-v1.0.5'+('-'+sha[:7] if updated else '')+'.txt',(digest+'  '+name+'\n').encode(),'text/plain')]:
  if filename in existing:
   assert existing[filename]['size']==len(data)
   continue
  request('POST',release['upload_url'].split('{')[0]+'?name='+filename,data,mime)
 print(release['html_url'],name,digest)
if __name__=='__main__':main()
