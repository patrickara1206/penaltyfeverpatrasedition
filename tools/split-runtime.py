"""Keep the portable WASM fetch bridge below Cloudflare's per-asset limit."""
from pathlib import Path
import json
app=Path(__file__).resolve().parents[1]/'app';p=app/'wasm-local.js';s=p.read_text(encoding='utf8')
if 'const assets={'not in s:raise SystemExit('Runtime already split; no change')
start=s.index('const assets=')+len('const assets=');assets,end=json.JSONDecoder().raw_decode(s[start:]);bridge=s[start+end:]
folder=app/'runtime';folder.mkdir(exist_ok=True);names=[];n=0
for key,value in assets.items():
 for offset in range(0,len(value),8_000_000):
  n+=1;name='runtime/wasm-'+str(n).zfill(2)+'.js';names.append(name)
  code='window.PF_WASM_ASSETS=window.PF_WASM_ASSETS||{};\nwindow.PF_WASM_ASSETS['+json.dumps(key)+']'+('='if offset==0 else'+=')+json.dumps(value[offset:offset+8_000_000])+';\n'
  (app/name).write_text(code,encoding='utf8')
p.write_text('(function(){const assets=window.PF_WASM_ASSETS'+bridge,encoding='utf8')
index=app/'index.html';html=index.read_text(encoding='utf8');html=html.replace('<script src="wasm-local.js">',''.join('<script src="'+x+'"></script>'for x in names)+'<script src="wasm-local.js">');index.write_text(html,encoding='utf8')
print('Split WASM into',len(names),'assets; original encoded bytes unchanged')
