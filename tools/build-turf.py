"""Deterministic grass material, generated from blades and multiscale color noise."""
from pathlib import Path
import argparse,random,struct,zlib,sys
p=argparse.ArgumentParser();p.add_argument('--deps');a=p.parse_args()
if a.deps:sys.path.insert(0,str(Path(a.deps).resolve()))
from PIL import Image,ImageDraw,ImageFilter
base=Path(__file__).resolve().parents[1];rng=random.Random(20261102)
w,h=1200,594
layers=[]
for size in [(17,9),(70,35),(300,150)]:
 im=Image.new('L',size);im.putdata([rng.randrange(55,200)for _ in range(size[0]*size[1])]);layers.append(im.resize((w,h),Image.Resampling.BICUBIC))
noise=[im.tobytes()for im in layers];image=Image.new('RGB',(w,h));pixels=image.load();bands=[0,50,110,182,268,366,476,594]
for y in range(h):
 band=next((i for i in range(7)if bands[i]<=y<bands[i+1]),6);mow=1.035 if band%2 else .965
 for x in range(w):
  at=y*w+x;n=(noise[0][at]-128)*.10+(noise[1][at]-128)*.06+(noise[2][at]-128)*.045+rng.uniform(-4,4)
  pixels[x,y]=(max(0,round((35+n*.4)*mow)),max(0,round((106+n)*mow)),max(0,round((48+n*.48)*mow)))
draw=ImageDraw.Draw(image,'RGBA')
for _ in range(82000):
 x=rng.randrange(w);y=rng.randrange(h);length=1+y/h*3;lean=rng.uniform(-1.5,1.5);light=rng.random()>.56
 draw.line([(x,y),(x+lean,y-length)],fill=(141,169,87,35)if light else(8,48,25,45),width=1)
for _ in range(3200):
 x=rng.randrange(w);y=rng.randrange(h);draw.point((x,y),fill=(192,180,111,40))
image=image.filter(ImageFilter.GaussianBlur(.25));preview=base/'previas/turf-2026.png';image.save(preview)
rgb=image.tobytes();argb=bytearray()
for i in range(0,len(rgb),3):argb.extend((255,rgb[i],rgb[i+1],rgb[i+2]))
def tag(t,b):return struct.pack('<HI',(t<<6)|63,len(b))+b
payload=tag(36,struct.pack('<HBHH',29000,5,w,h)+zlib.compress(argb,9))
payload+=tag(56,struct.pack('<HH',1,29000)+b'pf_turf\0')
(base/'tools/actionscript/turf.bin').write_bytes(payload)
print('Grass material',w,h,len(payload),'bytes')
