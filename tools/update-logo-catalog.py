"""Refresh attributable catalogue crests; never guess a club from a fuzzy name."""
from pathlib import Path
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor,as_completed
import urllib.request,json,unicodedata,re,hashlib,datetime
app=Path(__file__).resolve().parents[1]/'app'
countries={'Brasil':'brazil','Estados Unidos':'usa','Argentina':'argentina','México':'mexico','Inglaterra':'england','Espanha':'spain','Alemanha':'germany','França':'france','Itália':'italy','Portugal':'portugal','Arábia Saudita':'saudi-arabia','Colômbia':'colombia','Uruguai':'uruguay','Equador':'ecuador','Japão':'japan','Rússia':'russia','África do Sul':'south-africa','Egito':'egypt'}
def fetch(url):
 req=urllib.request.Request(url,headers={'User-Agent':'PF-Catalogue-Update/1.0'})
 with urllib.request.urlopen(req,timeout=25)as r:return r.read()
def norm(s):return re.sub('[^a-z0-9]','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())
class Catalog(HTMLParser):
 def __init__(self):super().__init__();self.rows=[]
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='img' and '/256x256/'in a.get('src','') and a.get('alt'):self.rows.append((a['alt'].removesuffix(' logo').removesuffix(' Logo'),a['src']))
data=json.loads((app/'data.json').read_text(encoding='utf8'));logos=json.loads((app/'logos.js').read_text(encoding='utf8').split('=',1)[1].strip().rstrip(';'));manifest=json.loads((app/'logos-manifest.json').read_text(encoding='utf8'));catalogs={};errors=[]
with ThreadPoolExecutor(max_workers=8)as ex:
 jobs={ex.submit(fetch,'https://football-logos.cc/'+c+'/'):c for c in countries.values()}
 for job in as_completed(jobs):
  country=jobs[job]
  try:p=Catalog();p.feed(job.result().decode('utf8'));catalogs[country]=p.rows
  except Exception as e:errors.append({'country':country,'error':str(e)[:120]})
requests={};matches={}
for c in data['competitions']:
 country=countries.get(c.get('country'))
 if not country or c.get('historical'):continue
 for team in c['teams']:
  choices=[(name,url)for name,url in catalogs.get(country,[])if norm(name)==norm(team)]
  if len(set(u for _,u in choices))==1:
   name,url=choices[0];matches[team]={'name':name,'url':url,'source':'https://football-logos.cc/'+country+'/','country':country}
for team,row in matches.items():requests[row['url']]=row
downloaded={}
with ThreadPoolExecutor(max_workers=12)as ex:
 jobs={ex.submit(fetch,url):url for url in requests}
 for job in as_completed(jobs):
  url=jobs[job]
  try:
   b=job.result()
   if not b.startswith(b'\x89PNG\r\n\x1a\n'):raise ValueError('Not PNG')
   file='assets/logos/'+hashlib.sha256(url.encode()).hexdigest()[:16]+'.png';(app/file).write_bytes(b);downloaded[url]=file
  except Exception as e:errors.append({'url':url,'error':str(e)[:120]})
updated=[]
for team,row in matches.items():
 if row['url']in downloaded:
  row.update(path=downloaded[row['url']],checked_at='2026-10-29');logos['teams'][team]=row['path'];manifest['teams'][team]=row;updated.append(team)
(app/'logos.js').write_text('window.PF_LOGOS='+json.dumps(logos,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf8')
(app/'logos-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
current=set(n for c in data['competitions']if not c.get('historical')for n in c['teams']);pending=sorted(n for n in current if '/edition/'in logos['teams'].get(n,''))
report={'checked_at':'2026-10-29','source':'football-logos.cc (third-party catalogue; not official certification)','refreshed':updated,'unverified_monograms':pending,'errors':errors,'limitations':'No claim that every crest is the latest official 2026 mark. Historical editions retain their artwork.'}
(app/'logo-audit-v105.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'refreshed':len(updated),'monograms_remaining':len(pending),'errors':len(errors)}))
