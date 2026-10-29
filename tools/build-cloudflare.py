"""Create a public static bundle, without source tools, saves or duplicate crests."""
from pathlib import Path
import shutil,json,zipfile,sys,re,base64
repo=Path(__file__).resolve().parents[1];app=repo/'app';out=(repo/sys.argv[1]).resolve()if len(sys.argv)>1 else repo.parents[1]/'outputs'/'cloudflare-v105';out.mkdir(parents=True,exist_ok=True)
files=[]
for p in app.iterdir():
 if (p.is_file()and p.suffix in ['.js','.css','.svg','.png','.swf']or p.name=='index.html')and p.name not in ['logos-embedded.js','wasm-local.js']:files.append((p,p.name))
logos=json.loads((app/'logos.js').read_text(encoding='utf8').split('=',1)[1].strip().rstrip(';'))
for rel in sorted(set(logos['teams'].values())|set(logos['competitions'].values())):files.append((app/rel,rel))
for p,rel in files:
 assert p.stat().st_size<25*1024*1024,(p.name,p.stat().st_size)
 dest=out/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
# On the web, fetch only visible crests and the selected WASM module on demand.
# The portable app retains its embedded resources and strict connect-src 'none'.
index=(out/'index.html').read_text(encoding='utf8')
index=re.sub(r'<script src="runtime/wasm-\d+\.js"></script>','',index)
index=re.sub(r'<script src="(?:wasm-local|logos-embedded)\.js(?:\?[^"]*)?"></script>','',index)
index=index.replace("connect-src 'none'","connect-src 'self'")
(out/'index.html').write_text(index,encoding='utf8')
modules={}
for p in sorted((app/'runtime').glob('*.js')):
 text=p.read_text(encoding='utf8');m=re.search(r'window.PF_WASM_ASSETS\[("[^"]+")\](\+?=)(".*");',text)
 assert m,p.name
 key=json.loads(m[1]);modules[key]=modules.get(key,'')+json.loads(m[3])
for name,value in modules.items():
 binary=base64.b64decode(value);assert binary.startswith(b'\0asm')and len(binary)<25*1024*1024
 (out/name).write_bytes(binary)
(out/'_headers').write_text('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n  X-Frame-Options: DENY\n',encoding='utf8')
archive=out.parent/'Cloudflare-Penalty-Fever-v1.0.5.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=7)as z:
 allowed={rel for _,rel in files}|set(modules)|{'_headers'}
 for rel in sorted(allowed):z.write(out/rel,rel)
with zipfile.ZipFile(archive)as z:assert z.testzip()is None
print(json.dumps({'directory':str(out),'zip':str(archive),'files':len(allowed),'bytes':archive.stat().st_size,'web':'on-demand crests and WASM; portable resources unchanged'}))
