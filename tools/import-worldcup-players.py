"""Import sourced World Cup squad names; derivative dataset CC BY-SA 4.0."""
import csv,json,collections,unicodedata
from pathlib import Path
repo=Path(__file__).resolve().parents[1];cache=repo.parent/'research-v109'
translate=dict(x.split('=') for x in "Algeria=Argélia|Australia=Austrália|Austria=Áustria|Belgium=Bélgica|Bolivia=Bolívia|Bosnia and Herzegovina=Bosnia and Herzegovina|Brazil=Brasil|Bulgaria=Bulgária|Cameroon=Camarões|Canada=Canadá|Colombia=Colômbia|Czech Republic=República Tcheca|Czechoslovakia=Tchecoslováquia|Denmark=Dinamarca|Dutch East Indies=Índias Orientais Holandesas|East Germany=Alemanha Oriental|Ecuador=Equador|Egypt=Egito|England=Inglaterra|France=França|Germany=Alemanha|Ghana=Gana|Greece=Grécia|Hungary=Hungria|Iceland=Islândia|Iran=Irã|Iraq=Iraque|Italy=Itália|Ivory Coast=Costa do Marfim|Japan=Japão|Mexico=México|Morocco=Marrocos|Netherlands=Países Baixos|New Zealand=Nova Zelândia|Nigeria=Nigéria|North Korea=Coreia do Norte|Northern Ireland=Irlanda do Norte|Norway=Noruega|Panama=Panamá|Poland=Polônia|Qatar=Catar|Republic of Ireland=Irlanda|Romania=Romênia|Russia=Rússia|Saudi Arabia=Arábia Saudita|Scotland=Escócia|Serbia=Sérvia|Serbia and Montenegro=Sérvia e Montenegro|Slovakia=Eslováquia|Slovenia=Eslovênia|South Africa=África do Sul|South Korea=Coreia do Sul|Soviet Union=União Soviética|Spain=Espanha|Sweden=Suécia|Switzerland=Suíça|Trinidad and Tobago=Trinidad e Tobago|Tunisia=Tunísia|Turkey=Turquia|Ukraine=Ucrânia|United Arab Emirates=Emirados Árabes Unidos|United States=Estados Unidos|Wales=País de Gales|West Germany=Alemanha Ocidental|Yugoslavia=Iugoslávia".split('|'))
def read(n):return list(csv.DictReader((cache/(n+'.csv')).open(encoding='utf-8-sig')))
penalties=collections.defaultdict(list)
translate.update({'Uruguay':'Uruguai','Paraguay':'Paraguai','Croatia':'Croácia'})
for r in read('penalty_kicks'):
 if "Men's" in r['tournament_name']:penalties[(r['tournament_id'],r['team_id'])].append(r)
out={};ids={}
for r in read('squads'):
 if "Men's" not in r['tournament_name']:continue
 year=r['tournament_id'][-4:];team=translate.get(r['team_name'],r['team_name']);key=year+'::'+team
 name=' '.join(x for x in [r['given_name'],r['family_name']] if x not in ['not applicable','NA',''])
 player={'name':name,'number':int(r['shirt_number']),'role':'Goleiro' if r['position_code']=='GK' else 'Cobrador','id':r['player_id']}
 out.setdefault(key,{'players':[],'source':'https://github.com/jfjelstul/worldcup','year':int(year),'verified':True,'orderVerified':False})['players'].append(player);ids[key]=(r['tournament_id'],r['team_id'])
for key,v in out.items():
 rows=penalties.get(ids[key],[])
 if rows:
  latest=max(r['match_date'] for r in rows);rows=[r for r in rows if r['match_date']==latest];order=[r['player_id'] for r in rows]
  v['players'].sort(key=lambda p:(order.index(p['id']) if p['id'] in order else 1000+(p['role']=='Goleiro'),p['number']))
  v['orderVerified']=True;v['orderDate']=latest;v['penaltyOrderIds']=order
 else:v['players'].sort(key=lambda p:(p['role']=='Goleiro',p['number']))
# FR Yugoslavia is the catalog label for Yugoslavia in 1998, not modern Serbia.
if '1998::Iugoslávia'in out:out['1998::FR Yugoslavia']=out['1998::Iugoslávia']
(repo/'app/worldcup-players.js').write_text('window.ME_WORLD_CUP='+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf8')
data=json.loads((repo/'app/data.json').read_text(encoding='utf8'));expected=[c['season']+'::'+n for c in data['competitions']if c['id'].startswith('world-')for n in c['teams']];missing=[k for k in expected if k not in out]
(repo/'app/worldcup-coverage.json').write_text(json.dumps({'source':'https://github.com/jfjelstul/worldcup','license':'CC BY-SA 4.0','checkedAt':'2026-11-05','teams':len(expected),'covered':sum(k in out for k in expected),'missing':missing},ensure_ascii=False,indent=2),encoding='utf8')
print('World Cup squads',len(out),'catalog coverage',len(expected)-len(missing),'/',len(expected),'missing',missing)
