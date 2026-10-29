"""Build a portable ZIP with CRC and content verification; no installation required."""
from pathlib import Path
import json,shutil,zipfile,hashlib
repo=Path(__file__).resolve().parents[1]
name='Penalty-Fever-2026-Edition-v1.0.5'
output=repo.parents[1]/'outputs';output.mkdir(exist_ok=True)
folder=output/name;folder.mkdir(exist_ok=True)
artwork_manifest=json.loads((repo/'app/logos-manifest.json').read_text(encoding='utf8'))
referenced_artwork={'app/'+row['path']for rows in artwork_manifest.values()for row in rows.values()}
files=[]
for p in sorted(repo.rglob('*')):
 rel=p.relative_to(repo)
 if not p.is_file()or any(x in ['.git','distribuicao','__pycache__','node_modules','dist-cloudflare','.wrangler']for x in rel.parts)or p.name.startswith('.env')or p.suffix in ['.pyc','.log']:continue
 if p.name.startswith('Cloudflare-Penalty-Fever-')and p.suffix=='.zip':continue
 # Replaced catalogue files remain in Git history, but the portable game only
 # needs the images referenced by its current manifest (including fallbacks).
 is_catalog_image=rel.as_posix().startswith('app/assets/logos/')or(rel.as_posix().startswith('app/assets/edition/')and p.name.startswith(('team-','competition-')))
 if is_catalog_image:
  if rel.as_posix()not in referenced_artwork:continue
 if p.name.startswith('qa-'):raise RuntimeError('Temporary QA file in package')
 files.append((p,rel));dest=folder/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
manifest=json.loads((repo/'app/logos-manifest.json').read_text(encoding='utf8'))
for rows in manifest.values():
 for row in rows.values():assert (repo/'app'/row['path']).is_file(),row['path']
archive=output/(name+'.zip')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=7)as z:
 for p,rel in files:z.write(p,name+'/'+rel.as_posix())
with zipfile.ZipFile(archive)as z:
 assert z.testzip()is None
 expected={name+'/'+rel.as_posix()for p,rel in files};assert set(z.namelist())==expected
 assert name+'/JOGAR.html'in expected
 assert 'v1.0.5'in z.read(name+'/app/index.html').decode('utf8')
 for p,rel in files:assert hashlib.sha256(z.read(name+'/'+rel.as_posix())).digest()==hashlib.sha256(p.read_bytes()).digest()
digest=hashlib.sha256(archive.read_bytes()).hexdigest();dist=repo/'distribuicao';dist.mkdir(exist_ok=True);shutil.copy2(archive,dist/'Penalty-Fever-2026-Edition.zip');(dist/'SHA256.txt').write_text(digest+'  Penalty-Fever-2026-Edition.zip\n',encoding='utf8');(output/(name+'.sha256')).write_text(digest+'  '+archive.name+'\n',encoding='utf8')
print(json.dumps({'zip':str(archive),'bytes':archive.stat().st_size,'files':len(files),'sha256':digest},indent=2))
