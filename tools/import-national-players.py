"""Import edition-specific national squads, validating provider season."""
import urllib.request,json,concurrent.futures
from pathlib import Path
repo=Path(__file__).resolve().parents[1];cache=repo.parent/'research-v109'/'national';cache.mkdir(parents=True,exist_ok=True)
translate={'Albania':'Albânia','Austria':'Áustria','Belgium':'Bélgica','Croatia':'Croácia','Czechia':'Tchéquia','Czech Republic':'República Tcheca','Denmark':'Dinamarca','England':'Inglaterra','France':'França','Georgia':'Geórgia','Germany':'Alemanha','Hungary':'Hungria','Italy':'Itália','Netherlands':'Países Baixos','Poland':'Polônia','Romania':'Romênia','Scotland':'Escócia','Serbia':'Sérvia','Slovakia':'Eslováquia','Slovenia':'Eslovênia','Spain':'Espanha','Switzerland':'Suíça','Turkey':'Turquia','Ukraine':'Ucrânia','Brazil':'Brasil','Bolivia':'Bolívia','Canada':'Canadá','Colombia':'Colômbia','Costa Rica':'Costa Rica','Ecuador':'Equador','Mexico':'México','Paraguay':'Paraguai','United States':'Estados Unidos','Uruguay':'Uruguai','Algeria':'Argélia','Australia':'Austrália','Cape Verde':'Cabo Verde','Congo DR':'RD Congo','Curacao':'Curaçao','Egypt':'Egito','Ghana':'Gana','Iran':'Irã','Iraq':'Iraque','Ivory Coast':'Costa do Marfim','Japan':'Japão','Jordan':'Jordânia','Morocco':'Marrocos','New Zealand':'Nova Zelândia','Norway':'Noruega','Panama':'Panamá','Qatar':'Catar','Saudi Arabia':'Arábia Saudita','Senegal':'Senegal','South Africa':'África do Sul','South Korea':'Coreia do Sul','Tunisia':'Tunísia','Uzbekistan':'Uzbequistão','Wales':'País de Gales'}
translate.update({'Türkiye':'Turquia','Sweden':'Suécia','Bosnia and Herzegovina':'Bósnia e Herzegovina','Bosnia-Herzegovina':'Bósnia e Herzegovina'})
def fetch(u,key):
 f=cache/(key+'.json')
 if f.exists():return json.loads(f.read_text(encoding='utf8'))
 try:
  d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'MarcaEterna/1.0.9'}),timeout=25));f.write_text(json.dumps(d,ensure_ascii=False),encoding='utf8');return d
 except:return{}
tasks=[]
for code,year in [('uefa.euro',2024),('conmebol.america',2024),('fifa.world',2026)]:
 d=fetch('https://site.api.espn.com/apis/site/v2/sports/soccer/'+code+'/teams?season='+str(year)+'&limit=100','teams-'+code+'-'+str(year))
 for sport in d.get('sports',[]):
  for league in sport.get('leagues',[]):
   for row in league.get('teams',[]):tasks.append((code,year,row['team']))
def roster(task):
 code,year,t=task;u='https://site.api.espn.com/apis/site/v2/sports/soccer/'+code+'/teams/'+t['id']+'/roster?season='+str(year);d=fetch(u,'roster-'+code+'-'+t['id']+'-'+str(year))
 if d.get('season',{}).get('year')!=year:return None
 players=[]
 for a in d.get('athletes',[]):
  for x in a.get('items',[a]):
   if x.get('displayName'):players.append({'id':str(x['id']),'name':x['displayName'],'number':int(x.get('jersey','0'))if str(x.get('jersey','0')).isdigit()else 0,'role':'Goleiro'if x.get('position',{}).get('abbreviation')=='G'else'Cobrador'})
 name=translate.get(t['displayName'],t['displayName'])
 return str(year)+'::'+name,{'players':players,'year':year,'source':u,'verified':True,'orderVerified':False,'consultedAt':'2026-11-05'}if len(players)>=11 else None
out={}
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
 for item in pool.map(roster,tasks):
  if item and item[1]:out[item[0]]=item[1]
for a,b in [('2024::Albânia','2024::Albania'),('2024::Geórgia','2024::Georgia'),('2024::Tchéquia','2024::República Tcheca')]:
 if a in out:out[b]=out[a]
data=json.loads((repo/'app/data.json').read_text(encoding='utf8'));expected=[str(c['season'])+'::'+n for c in data['competitions']if c['id']in ['world','euro','copa-america']for n in c['teams']]
(repo/'app/national-players.js').write_text('window.ME_NATIONAL_PLAYERS='+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf8')
(repo/'app/national-players-coverage.json').write_text(json.dumps({'expected':len(expected),'covered':sum(k in out for k in expected),'missing':[k for k in expected if k not in out]},ensure_ascii=False,indent=2),encoding='utf8');print('National squads',len(out),'of',len(expected),'missing',[k for k in expected if k not in out],flush=True)
