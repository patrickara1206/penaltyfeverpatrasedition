"""Embed the catalog artwork so file-origin browsers do not need separate image requests."""
from pathlib import Path
import json,base64,hashlib
root=Path(__file__).resolve().parents[1];app=root/'app'
logos=json.loads((app/'logos.js').read_text(encoding='utf-8').split('=',1)[1].strip().rstrip(';'))
paths=sorted(set(p for rows in logos.values()for p in rows.values())|{'trophy.svg'})
images={}
for rel in paths:
 p=(app/rel).resolve();assert p.is_relative_to(app.resolve());mime={'.png':'image/png','.webp':'image/webp','.svg':'image/svg+xml'}[p.suffix];raw=p.read_bytes();value='data:'+mime+';base64,'+base64.b64encode(raw).decode('ascii');assert base64.b64decode(value.split(',',1)[1])==raw;images[rel]=value
temporary=app/'logos-embedded.tmp'
temporary.write_text('window.PF_EMBEDDED_LOGOS='+json.dumps(images,separators=(',',':'))+';\n',encoding='utf-8')
temporary.replace(app/'logos-embedded.js')
print(json.dumps({'images':len(images),'scriptBytes':(app/'logos-embedded.js').stat().st_size},indent=2))
