"""Shape localized Flash labels with Noto/HarfBuzz, then bake portable SWF bitmaps.
Build-only dependencies: Pillow, uharfbuzz, freetype-py. No runtime font requests.
"""
from pathlib import Path
import sys,argparse,ast,re,struct,zlib,json,hashlib
p=argparse.ArgumentParser();p.add_argument('--fonts',required=True);p.add_argument('--deps');args=p.parse_args()
if args.deps:sys.path.insert(0,str(Path(args.deps).resolve()))
from PIL import Image
import freetype,uharfbuzz as hb
base=Path(__file__).resolve().parents[1];fonts=Path(args.fonts);source=(base/'app/settings.js').read_text(encoding='utf8');locales=['pt','en','es','fr','de','it','zh','ar','hi','ru'];tags=bytearray();exports=[];report=[]
def tag(t,b):return struct.pack('<HI',(t<<6)|63,len(b))+b
for key in ['round','attack','defend']:
 labels=ast.literal_eval('['+re.search(r'\b'+key+r':\[(.*?)\],',source,re.S).group(1)+']')
 for index,(lang,text)in enumerate(zip(locales,labels)):
  family={'zh':'notosanssc','ar':'notonaskharabic','hi':'notosansdevanagari'}.get(lang,'notosans');fontfile=fonts/(family+'.ttf');size=24 if key=='round'else 30
  face=freetype.Face(str(fontfile));face.set_pixel_sizes(0,size);font=hb.Font(hb.Face(fontfile.read_bytes()));font.scale=(size*64,size*64);hb.ot_font_set_funcs(font);buf=hb.Buffer();buf.add_str(text);buf.guess_segment_properties();hb.shape(font,buf)
  assert all(g.codepoint for g in buf.glyph_infos),(lang,text,'missing glyph')
  image=Image.new('RGBA',(1400,150));x=20;y=95
  for info,pos in zip(buf.glyph_infos,buf.glyph_positions):
   face.load_glyph(info.codepoint,freetype.FT_LOAD_RENDER);g=face.glyph;b=g.bitmap
   if b.width and b.rows:
    mask=Image.frombytes('L',(b.width,b.rows),bytes(b.buffer),'raw','L',b.pitch);glyph=Image.new('RGBA',mask.size,(255,255,255,255));glyph.putalpha(mask);image.alpha_composite(glyph,(round(x+pos.x_offset/64+g.bitmap_left),round(y-pos.y_offset/64-g.bitmap_top)))
   x+=pos.x_advance/64;y-=pos.y_advance/64
  bbox=image.getbbox();assert bbox;image=image.crop((max(0,bbox[0]-2),max(0,bbox[1]-2),bbox[2]+2,bbox[3]+2));w,h=image.size
  # DefineBitsLossless2 stores premultiplied ARGB pixels.
  rgba=image.tobytes();argb=bytearray()
  for at in range(0,len(rgba),4):
   r,g,b,a=rgba[at:at+4];argb+=bytes([a,r*a//255,g*a//255,b*a//255])
  id=2000+len(exports);name='pf_'+lang+'_'+key;tags+=tag(36,struct.pack('<HBHH',id,5,w,h)+zlib.compress(argb));exports.append((id,name));report.append({'language':lang,'key':key,'text':text,'width':w,'height':h,'font':family})
  preview=base/'previas'/'text-labels';preview.mkdir(parents=True,exist_ok=True);image.save(preview/(name+'.png'))
tags+=tag(56,struct.pack('<H',len(exports))+b''.join(struct.pack('<H',id)+name.encode()+b'\0'for id,name in exports))
(base/'tools/actionscript/text-labels.bin').write_bytes(tags);(base/'tools/actionscript/text-labels.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
license_dir=base/'licenses'/'noto';license_dir.mkdir(parents=True,exist_ok=True)
for file in fonts.glob('*OFL.txt'):(license_dir/file.name).write_bytes(file.read_bytes())
print('Baked',len(exports),'shaped labels;',len(tags),'bytes; zero missing glyphs')
