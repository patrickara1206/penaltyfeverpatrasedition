"""Create a public static bundle, without source tools, saves or duplicate crests."""
from pathlib import Path
import shutil,json,zipfile,sys
repo=Path(__file__).resolve().parents[1];app=repo/'app';out=(repo/sys.argv[1]).resolve()if len(sys.argv)>1 else repo.parents[1]/'outputs'/'cloudflare-v105';out.mkdir(parents=True,exist_ok=True)
files=[]
for p in app.iterdir():
 if p.is_file()and p.suffix in ['.js','.css','.svg','.png','.swf']or p.name=='index.html':files.append((p,p.name))
for p in (app/'runtime').glob('*.js'):files.append((p,'runtime/'+p.name))
for p,rel in files:
 assert p.stat().st_size<25*1024*1024,(p.name,p.stat().st_size)
 dest=out/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
(out/'_headers').write_text('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n  X-Frame-Options: DENY\n',encoding='utf8')
archive=out.parent/'Cloudflare-Penalty-Fever-v1.0.5.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=7)as z:
 for p in out.rglob('*'):
  if p.is_file():z.write(p,p.relative_to(out).as_posix())
with zipfile.ZipFile(archive)as z:assert z.testzip()is None
print(json.dumps({'directory':str(out),'zip':str(archive),'files':len(files)+1,'bytes':archive.stat().st_size}))
