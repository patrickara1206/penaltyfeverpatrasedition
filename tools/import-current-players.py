"""Refresh explicitly matched club rosters from public ESPN team pages/API."""
from pathlib import Path
import urllib.request,json,concurrent.futures,unicodedata,re,time
repo=Path(__file__).resolve().parents[1];cache=repo.parent/'research-v109'/'espn';cache.mkdir(parents=True,exist_ok=True)
leagues=['bra.1','bra.2','bra.3','eng.1','eng.2','eng.3','esp.1','esp.2','esp.3','ger.1','ger.2','ger.3','fra.1','fra.2','fra.3','ita.1','ita.2','ita.3','arg.1','arg.2','usa.1','usa.2','mex.1','mex.2','por.1','por.2','ksa.1','col.1','col.2','uru.1','ecu.1','ecu.2','jpn.1','jpn.2','rus.1','rsa.1','egy.1','uefa.champions','uefa.europa','uefa.europa.conf']
def fetch(url,key):
 p=cache/(key+'.json')
 if p.exists():return json.loads(p.read_text(encoding='utf8'))
 req=urllib.request.Request(url,headers={'User-Agent':'MarcaEterna/1.0.9 public football catalogue'})
 try:
  with urllib.request.urlopen(req,timeout=25)as r:d=json.load(r)
  p.write_text(json.dumps(d,ensure_ascii=False),encoding='utf8');return d
 except Exception as e:return {'error':str(e)}
def norm(s):return re.sub('[^a-z0-9]','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())
data=json.loads((repo/'app/data.json').read_text(encoding='utf8'));clubs=set(n for c in data['competitions']if not c.get('historical')and c.get('region')!='Seleções'for n in c['teams'])
lookup={norm(n):n for n in clubs}
prefixes={'bra':'Brasil','eng':'Inglaterra','esp':'Espanha','ger':'Alemanha','fra':'França','ita':'Itália','arg':'Argentina','usa':'Estados Unidos','mex':'México','por':'Portugal','ksa':'Arábia Saudita','col':'Colômbia','uru':'Uruguai','ecu':'Equador','jpn':'Japão','rus':'Rússia','rsa':'África do Sul','egy':'Egito'}
by_country={country:set(n for c in data['competitions']if c.get('country')==country for n in c['teams'])for country in prefixes.values()}
alias={'tottenhamhotspur':'Tottenham','bayernmunich':'Bayern München','atleticomadrid':'Atlético de Madrid','athleticbilbao':'Athletic Club','brightonhovealbion':'Brighton','internazionalemilan':'Internazionale','internazionale':'Inter','parissaintgermain':'Paris Saint-Germain','manchesterunited':'Manchester United','bayer04leverkusen':'Bayer Leverkusen','fcbarcelona':'Barcelona','newyorkcityfc':'New York City','sportingcp':'Sporting','sportinglisbon':'Sporting','fenerbahce':'Fenerbahçe'}
matched={};unmatched=[]
def getleague(l):return l,fetch('https://site.api.espn.com/apis/site/v2/sports/soccer/'+l+'/teams?limit=500','teams-'+l)
with concurrent.futures.ThreadPoolExecutor(max_workers=5)as pool:
 for league,d in pool.map(getleague,leagues):
  for sp in d.get('sports',[]):
   for lg in sp.get('leagues',[]):
    for row in lg.get('teams',[]):
     t=row['team'];names=[t.get(k,'')for k in ['displayName','shortDisplayName','name','location']];hits={lookup[norm(n)]for n in names if norm(n)in lookup}
     hits|={alias[norm(n)]for n in names if norm(n)in alias and alias[norm(n)]in clubs}
     hits={n for n in hits if n in by_country.get(prefixes.get(league.split('.')[0]),set())}
     if len(hits)==1:
      name=hits.pop();matched.setdefault(name,{'id':t['id'],'league':league,'sourceName':t['displayName'],'source':'https://www.espn.com/soccer/team/_/id/'+t['id'],'logo':next((x['href']for x in t.get('logos',[])if 'default'in x.get('rel',[])),None)})
     else:unmatched.append({'id':t['id'],'names':names})
print('Matched clubs',len(matched),flush=True)
def roster(pair):
 name,t=pair;u='https://site.api.espn.com/apis/site/v2/sports/soccer/'+t['league']+'/teams/'+t['id']+'/roster';d=fetch(u,'roster-'+t['id']);players=[]
 for a in d.get('athletes',[]):
  if 'items'in a:athletes=a['items']
  else:athletes=[a]
  for x in athletes:
   if not x.get('displayName')or x.get('status',{}).get('type')not in [None,'active']:continue
   players.append({'id':x['id'],'name':x['displayName'],'number':int(x.get('jersey','0'))if str(x.get('jersey','0')).isdigit()else 0,'role':'Goleiro'if x.get('position',{}).get('abbreviation')=='G'else'Cobrador'})
 return name,{**t,'players':players,'consultedAt':'2026-11-05','season':d.get('season',{}).get('year'),'verified':True,'orderVerified':False}
out={}
with concurrent.futures.ThreadPoolExecutor(max_workers=5)as pool:
 for n,r in pool.map(roster,matched.items()):
  if len(r['players'])>=11 and r['season']==2026:out[n]=r
  if len(out)%50==0:print('Rosters',len(out),flush=True)
(repo/'app/current-players.js').write_text('window.ME_CURRENT_PLAYERS='+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf8')
coverage={'checkedAt':'2026-11-05','expectedClubs':len(clubs),'verifiedRosters':len(out),'players':sum(len(v['players'])for v in out.values()),'unverifiedClubs':sorted(clubs-set(out)),'verifiedPenaltyOrders':0,'penaltyOrderPolicy':'Only currently registered players present in a documented last shootout may receive a verified order. No order is inferred from shirt number.'}
(repo/'app/current-players-coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2),encoding='utf8')
(cache/'matched-clubs.json').write_text(json.dumps(matched,ensure_ascii=False,indent=2),encoding='utf8');(cache/'unmatched-source-clubs.json').write_text(json.dumps(unmatched,ensure_ascii=False),encoding='utf8')
print({k:v for k,v in coverage.items()if k!='unverifiedClubs'},flush=True)
