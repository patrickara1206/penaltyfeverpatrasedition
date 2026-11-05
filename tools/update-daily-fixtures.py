"""Refresh a public, dated fixture snapshot for portable play."""
from pathlib import Path
import urllib.request,json,datetime,concurrent.futures,sys
repo=Path(__file__).resolve().parents[1];day=sys.argv[1]if len(sys.argv)>1 else datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3))).strftime('%Y-%m-%d')
leagues=[['bra.1','Brasileirão Série A'],['bra.2','Brasileirão Série B'],['bra.3','Brasileirão Série C'],['bra.copa_do_brazil','Copa do Brasil'],['eng.1','Premier League'],['esp.1','LaLiga'],['ger.1','Bundesliga'],['ita.1','Serie A'],['fra.1','Ligue 1'],['por.1','Liga Portugal'],['arg.1','Argentina'],['usa.1','MLS'],['mex.1','Liga MX'],['conmebol.libertadores','Libertadores'],['conmebol.sudamericana','Sul-Americana'],['uefa.champions','Champions League'],['uefa.europa','Europa League']]
following=(datetime.date.fromisoformat(day)+datetime.timedelta(days=1)).isoformat()
def query(pair):
 code,label,query_day=pair;url='https://site.api.espn.com/apis/site/v2/sports/soccer/'+code+'/scoreboard?dates='+query_day.replace('-','');out=[]
 try:
  d=json.load(urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'MarcaEterna/1.0.9'}),timeout=20))
  for e in d.get('events',[]):
   comp=e.get('competitions',[{}])[0];teams=comp.get('competitors',[]);home=next((t for t in teams if t.get('homeAway')=='home'),None);away=next((t for t in teams if t.get('homeAway')=='away'),None)
   local_day=datetime.datetime.fromisoformat(e['date'].replace('Z','+00:00')).astimezone(datetime.timezone(datetime.timedelta(hours=-3))).strftime('%Y-%m-%d')
   if home and away and local_day==day:out.append({'id':str(e['id']),'date':e['date'],'home':home['team'].get('displayName',home['team']['name']),'away':away['team'].get('displayName',away['team']['name']),'league':label,'code':code,'source':url})
  return out,None
 except Exception as e:return [],{'league':code,'error':str(e)}
fixtures=[];errors=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
 for rows,error in pool.map(query,[(code,label,d)for code,label in leagues for d in [day,following]]):
  fixtures.extend(rows)
  if error:errors.append(error)
fixtures=list({r['id']:r for r in fixtures}.values())
payload={'date':day,'timezone':'America/Sao_Paulo','consultedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'leagues':leagues,'fixtures':sorted(fixtures,key=lambda x:x['date']),'errors':errors,'scope':'Somente as competições retornadas pelo provedor consultado.'}
(repo/'app/day-fixtures.js').write_text('window.ME_DAY_FIXTURES='+json.dumps(payload,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf8');print('Snapshot',day,len(fixtures),'games',len(errors),'source errors')
