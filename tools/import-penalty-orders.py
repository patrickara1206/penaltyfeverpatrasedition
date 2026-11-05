"""Use documented shootout IDs; intersect with the current sourced roster."""
from pathlib import Path
import urllib.request,json,concurrent.futures,datetime
repo=Path(__file__).resolve().parents[1];cache=repo.parent/'research-v109'/'orders';cache.mkdir(parents=True,exist_ok=True)
p=repo/'app/current-players.js';data=json.loads(p.read_text(encoding='utf8').split('=',1)[1].strip().rstrip(';'))
def fetch(url,key):
 f=cache/(key+'.json')
 if f.exists():return json.loads(f.read_text(encoding='utf8'))
 try:
  d=json.load(urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'MarcaEterna/1.0.9'}),timeout=20));f.write_text(json.dumps(d,ensure_ascii=False),encoding='utf8');return d
 except Exception:return{}
def one(pair):
 name,r=pair;events=[]
 for season in [2026,2025]:
  url='https://site.api.espn.com/apis/site/v2/sports/soccer/all/teams/'+r['id']+'/schedule?season='+str(season);d=fetch(url,'schedule-'+r['id']+'-'+str(season))
  for e in d.get('events',[]):
   if e.get('date','')>'2026-11-05T23:59:59Z':continue
   c=e.get('competitions',[{}])[0]
   if c.get('status',{}).get('type',{}).get('completed')and (c.get('status',{}).get('type',{}).get('name')=='STATUS_FINAL_PEN'or any(x.get('shootoutScore')is not None for x in c.get('competitors',[]))):events.append(e)
  if events:break
 if not events:return name,r
 e=max(events,key=lambda x:x['date']);code=e.get('league',{}).get('slug')or r['league'];url='https://site.api.espn.com/apis/site/v2/sports/soccer/'+code+'/summary?event='+str(e['id']);d=fetch(url,'summary-'+str(e['id']))
 side=next((x for x in d.get('shootout',[])if str(x.get('id'))==r['id']),None)
 if not side:return name,r
 members={x['id']for x in r['players']};order=[str(x['playerId'])for x in sorted(side.get('shots',[]),key=lambda x:x['shotNumber'])if str(x.get('playerId'))in members]
 order=list(dict.fromkeys(order))
 if not order:return name,r
 r['penaltyOrderIds']=order;r['orderVerified']=True;r['orderDate']=e['date'][:10];r['orderSource']=url;r['orderScope']='Latest shootout located in source calendars 2026/2025; only players still listed in the current roster.'
 r['players'].sort(key=lambda x:order.index(x['id'])if x['id']in order else 1000)
 return name,r
out={};count=0
with concurrent.futures.ThreadPoolExecutor(max_workers=5)as pool:
 for n,r in pool.map(one,data.items()):
  out[n]=r
  if r.get('orderVerified'):count+=1
  if len(out)%50==0:print('Checked',len(out),'confirmed orders',count,flush=True)
p.write_text('window.ME_CURRENT_PLAYERS='+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf8')
report=repo/'app/current-players-coverage.json';d=json.loads(report.read_text(encoding='utf8'));d['verifiedPenaltyOrders']=count;d['penaltyOrderCoverage']='Only the latest shootout returned by source calendars 2026/2025. Unlisted players have no inferred order.';report.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8');print('Confirmed orders',count,'of',len(out),flush=True)
