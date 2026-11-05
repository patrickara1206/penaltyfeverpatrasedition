"""Package documented trophy photographs with reusable licence attribution."""
from pathlib import Path
import json, urllib.request, urllib.parse, re, html, base64
repo=Path(__file__).resolve().parents[1]
cache=repo.parent/'research-v109'
pages=json.loads((cache/'trophy-metadata.json').read_text(encoding='utf8'))['query']['pages']
photos={
 'File:Conmebol Copa Libertadores Trophy45013.png':(['lib','cont-south'],'Libertadores'),
 'File:FIFA World Cup Trophy photo by Djuradj Vujcic.jpg':(['world','national-world'],'Copa do Mundo de seleções'),
 'File:Troféu Campeonato Brasileiro 2024.jpg':(['br0'],'Brasileirão Série A · modelo fotografado em 2024'),
 'File:UEFA Champions LeagueTrophy7612.png':(['ucl','cont-europe'],'Champions League'),
}
extra={
 'File:Premier League Trophy at Manchester\'s National Football Museum (Ank Kumar) 02.jpg':(['eng'],'Premier League'),
 'File:Trophy of Fußball-Bundesliga in Singapore, 2023.jpg':(['ger'],'Bundesliga'),
 'File:UEFA Europa Conference League Trophy.jpg':(['uecl','cont-uecl'],'UEFA Conference League'),
}
url='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode({'action':'query','format':'json','prop':'imageinfo','titles':'|'.join(extra),'iiprop':'url|extmetadata','iiurlwidth':320})
try:
 data=json.load(urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'MarcaEterna/1.0.9'}),timeout=30))
 pages.update(data['query']['pages']);photos.update(extra)
except Exception as e:print('Additional photo metadata unavailable:',type(e).__name__)
out={};manifest=[]
for page in pages.values():
 if page.get('title')not in photos or not page.get('imageinfo'):continue
 ids,label=photos[page['title']];info=page['imageinfo'][0];meta=info['extmetadata'];license=meta.get('LicenseShortName',{}).get('value','')
 if license not in ['CC BY 2.0','CC BY-SA 4.0','CC BY 4.0','CC BY-SA 3.0','CC BY-SA 2.0']:continue
 imageurl=info.get('thumburl',info['url']).split('?')[0];file=cache/('trophy-'+ids[0]+Path(urllib.parse.urlparse(imageurl).path).suffix)
 try:
  if not file.exists():file.write_bytes(urllib.request.urlopen(urllib.request.Request(imageurl,headers={'User-Agent':'MarcaEterna/1.0.9'}),timeout=30).read())
  blob=file.read_bytes();mime='image/png'if blob.startswith(b'\x89PNG')else'image/jpeg'if blob.startswith(b'\xff\xd8')else None
  if not mime:raise ValueError('Unsupported image')
  row={'image':'data:'+mime+';base64,'+base64.b64encode(blob).decode(),'label':label,'author':html.unescape(re.sub('<[^>]+>','',meta.get('Artist',{}).get('value','Autor indicado na fonte'))),'source':info['descriptionurl'],'license':license,'licenseUrl':meta['LicenseUrl']['value']}
  for id in ids:out[id]=row
  manifest.append({k:v for k,v in row.items()if k!='image'})
 except Exception as e:print('Photo unavailable:',ids[0],type(e).__name__)
(repo/'app/trophies.js').write_text('window.ME_TROPHIES='+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf8')
(repo/'licenses/trophy-photos.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print('Documented trophy photographs:',len(manifest))
