"""Portable v1.0.9 package: runtime, licences, launcher, SHA-256 and CRC verification."""
from pathlib import Path
import json,zipfile,hashlib
repo=Path(__file__).resolve().parents[1];name='Na-Marca-v1.0.9';output=repo/'release-output';output.mkdir(exist_ok=True)
catalog=json.loads((repo/'app/logos-manifest.json').read_text(encoding='utf8'))
artwork={'app/'+r['path']for rows in catalog.values()for r in rows.values()}
files=[]
for top in ['app','licenses']:
 for p in sorted((repo/top).rglob('*')):
  if not p.is_file():continue
  rel=p.relative_to(repo).as_posix()
  if any(x in ['__pycache__','node_modules']for x in p.parts)or p.name.startswith(('.env','qa-'))or p.suffix in ['.log','.pyc']:continue
  if rel.startswith('app/assets/')and('/logos/'in rel or '/edition/'in rel)and p.name.startswith(('team-','competition-'))and rel not in artwork:continue
  if rel.startswith('app/assets/logos/')and rel not in artwork:continue
  if p.name=='marca-eterna.png':continue
  files.append((p,rel))
for rel in ['JOGAR.html','redirect.js','README.md','RELEASE-v1.0.9.md','DADOS-v1.0.9.md','LOGOS.md','CLUB-HISTORY.md']:
 p=repo/rel
 if p.exists():files.append((p,rel))
archive=output/(name+'.zip')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=7)as z:
 for p,rel in files:z.write(p,name+'/'+rel)
with zipfile.ZipFile(archive)as z:
 assert z.testzip()is None
 assert set(z.namelist())=={name+'/'+rel for p,rel in files}
 assert name+'/JOGAR.html'in z.namelist()
 assert 'v1.0.9'in z.read(name+'/app/index.html').decode('utf8')
 for p,rel in files:assert hashlib.sha256(z.read(name+'/'+rel)).digest()==hashlib.sha256(p.read_bytes()).digest(),rel
 for path in artwork:assert name+'/'+path in z.namelist(),path
digest=hashlib.sha256(archive.read_bytes()).hexdigest()
(output/'SHA256-v1.0.9.txt').write_text(digest+'  '+archive.name+'\n',encoding='utf8')
print(json.dumps({'zip':str(archive),'bytes':archive.stat().st_size,'files':len(files),'sha256':digest},indent=2))
