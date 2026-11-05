"""Publish a verified new v1.0.9 release using only the scoped CI credential."""
from pathlib import Path
import os,json,urllib.request,urllib.error,hashlib,subprocess,zipfile
REPO='patrickara1206/penaltyfeverpatrasedition';TAG='v1.0.9'
def request(method,path,data=None,mime='application/json'):
 url=path if path.startswith('https://uploads.github.com/repos/'+REPO+'/')else'https://api.github.com/repos/'+REPO+path
 req=urllib.request.Request(url,data=json.dumps(data).encode()if isinstance(data,dict)else data,method=method,headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json','Content-Type':mime,'User-Agent':'NaMarca-Releases'})
 try:
  with urllib.request.urlopen(req,timeout=180)as r:return json.load(r)
 except urllib.error.HTTPError as e:
  if e.code==404 and method=='GET':return None
  raise RuntimeError('GitHub HTTP '+str(e.code))from None
def main():
 assert os.environ.get('GITHUB_REPOSITORY')==REPO and os.environ.get('GITHUB_REF')=='refs/heads/'+TAG
 sha=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip();file=Path('release-output/Na-Marca-v1.0.9.zip');blob=file.read_bytes();digest=hashlib.sha256(blob).hexdigest()
 with zipfile.ZipFile(file)as z:
  assert z.testzip()is None
  assert 'NA MARCA'in z.read('Na-Marca-v1.0.9/app/index.html').decode('utf8')
 ref=request('GET','/git/ref/tags/'+TAG)
 if ref and ref['object']['sha']!=sha:raise RuntimeError('Existing tag belongs to another commit; preserved')
 release=request('GET','/releases/tags/'+TAG)
 if release is None:release=request('POST','/releases',{'tag_name':TAG,'target_commitish':sha,'name':'Na Marca · '+TAG,'body':Path('RELEASE-v1.0.9.md').read_text(encoding='utf8')+'\n\nCódigo: `'+sha+'`\n\nSHA-256: `'+digest+'`','draft':False,'prerelease':False,'make_latest':'true'})
 existing={a['name']:a for a in release['assets']}
 for name,data,mime in [(file.name,blob,'application/zip'),('SHA256-v1.0.9.txt',(digest+'  '+file.name+'\n').encode(),'text/plain')]:
  if name in existing:
   assert existing[name]['size']==len(data),'Asset already exists with different content; preserved'
   continue
  request('POST',release['upload_url'].split('{')[0]+'?name='+name,data,mime)
 print(release['html_url'],digest)
if __name__=='__main__':main()
