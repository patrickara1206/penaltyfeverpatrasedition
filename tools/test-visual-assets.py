"""Check portable artwork and the actual SWF actor frame hooks."""
from pathlib import Path
import json,struct,zlib,hashlib,xml.etree.ElementTree as ET

def image_info(path):
    data=path.read_bytes()
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        width,height=struct.unpack_from('>II',data,16);p=8;end=False
        while p<len(data):
            n=struct.unpack_from('>I',data,p)[0];kind=data[p+4:p+8];payload=data[p+8:p+8+n]
            assert len(payload)==n and zlib.crc32(kind+payload)&0xffffffff==struct.unpack_from('>I',data,p+8+n)[0],path
            p+=n+12
            if kind==b'IEND':end=True;break
        assert end,path
        return 'PNG',width,height
    if data.startswith(b'RIFF') and data[8:12]==b'WEBP':
        p=12
        while p+8<len(data):
            kind=data[p:p+4];n=struct.unpack_from('<I',data,p+4)[0];body=data[p+8:p+8+n]
            if kind==b'VP8X':return 'WEBP',1+int.from_bytes(body[4:7],'little'),1+int.from_bytes(body[7:10],'little')
            if kind==b'VP8L':
                bits=int.from_bytes(body[1:5],'little');return 'WEBP',1+(bits&0x3fff),1+((bits>>14)&0x3fff)
            if kind==b'VP8 ':
                assert body[3:6]==b'\x9d\x01\x2a',path
                return 'WEBP',struct.unpack_from('<H',body,6)[0]&0x3fff,struct.unpack_from('<H',body,8)[0]&0x3fff
            p+=8+n+(n%2)
    raise AssertionError('Unsupported/corrupted image: '+str(path))

base=Path(__file__).resolve().parents[1]
data=json.loads((base/'app/data.json').read_text(encoding='utf-8'))
manifest=json.loads((base/'app/logos-manifest.json').read_text(encoding='utf-8'))
expected=set(n for c in data['competitions'] for n in c['teams'])|set(data['nations'])
assert not expected-manifest['teams'].keys(),expected-manifest['teams'].keys()
assert not {c['id']for c in data['competitions']}-manifest['competitions'].keys()
files={row['path']for kind in manifest.values()for row in kind.values()}
formats={};sizes=[]
for rel in sorted(files):
 path=base/'app'/rel;assert path.is_file(),rel
 if path.suffix=='.svg':
  text=path.read_text(encoding='utf-8');root=ET.fromstring(text)
  assert root.tag.endswith('svg')
  assert '<script'not in text.lower() and 'onload='not in text.lower(),rel
  formats['SVG']=formats.get('SVG',0)+1
 else:
  format,width,height=image_info(path)
  assert width>=16 and height>=16,(rel,width,height)
  formats[format]=formats.get(format,0)+1
 sizes.append(path.stat().st_size)

raw=(base/'app/match.swf').read_bytes();d=b'FWS'+raw[3:8]+zlib.decompress(raw[8:]);nb=d[8]>>3;start=8+(5+4*nb+7)//8+4
def tags(data,start):
 p=start
 while p<len(data):
  v=struct.unpack_from('<H',data,p)[0];p+=2;t=v>>6;n=v&63
  if n==63:n=struct.unpack_from('<I',data,p)[0];p+=4
  b=data[p:p+n];p+=n;yield t,b
  if not t:break
actor=None;rootframe=0;hooks=set()
for t,b in tags(d,start):
 if t==39 and struct.unpack_from('<H',b)[0]==661:actor=b
 if t==12 and b'ppRecolor' in b:hooks.add(rootframe)
 if t==1:rootframe+=1
assert actor
previous=None;actor_frames=0
for t,b in tags(actor,4):
 if t==1:
  assert previous and previous[0]==12 and b'ppRecolor' in previous[1],actor_frames+1
  actor_frames+=1
 previous=t,b
assert actor_frames==20
assert {102,103,104,105,106}<=hooks,hooks
for brand in [b'CALMA+',b'ONDA',b'ARENA 12',b'RESENHA FM',b'PATRAS',b'RODADA ',b'ppPaintShots',b'patrasShot']:assert brand in d,brand
assert b'F E V E R   /   2 0 2 6' not in d
report={'status':'passed','teamsAndNations':len(expected),'competitions':len(data['competitions']),'artworkFiles':len(files),'formats':formats,'artworkBytes':sum(sizes),'actorFramesWithPostPlacementRecolor':actor_frames,'motionRootFramesWithRecolor':sorted(hooks),'matchSha256':hashlib.sha256(raw).hexdigest()}
(base/'VALIDACAO-VISUAL-ASSETS.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
