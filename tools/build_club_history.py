"""Build an offline, source-attributed history archive from public Wikipedia pages.
Unknown fields remain unknown. Counts are per competition, never a club total.
"""
from pathlib import Path
import concurrent.futures,hashlib,html,json,re,time,urllib.parse,urllib.request,unicodedata
BASE=Path(__file__).resolve().parents[1]
CACHE=BASE.parent/'club-history-cache';CACHE.mkdir(exist_ok=True)
UA={'User-Agent':'PatrasPenaltyResearch/1.0 (personal offline football history archive)'}
COUNTRIES={'brazil':['brazil','brazilian'],'england':['england','english'],'spain':['spain','spanish'],'germany':['germany','german'],'france':['france','french'],'italy':['italy','italian'],'argentina':['argentina','argentine'],'united-states':['american','united states'],'usa':['american','united states'],'mexico':['mexico','mexican'],'portugal':['portugal','portuguese'],'netherlands':['netherlands','dutch'],'greece':['greece','greek'],'belgium':['belgium','belgian'],'austria':['austria','austrian'],'scotland':['scotland','scottish'],'turkey':['turkey','turkish'],'norway':['norway','norwegian'],'bolivia':['bolivia','bolivian'],'chile':['chile','chilean'],'colombia':['colombia','colombian'],'ecuador':['ecuador','ecuadorian'],'paraguay':['paraguay','paraguayan'],'peru':['peru','peruvian'],'uruguay':['uruguay','uruguayan'],'venezuela':['venezuela','venezuelan']}
FETCH_COUNT=0
def req(url):
 global FETCH_COUNT
 key=hashlib.sha256(url.encode()).hexdigest();p=CACHE/(key+'.json')
 if p.exists():return json.loads(p.read_text(encoding='utf-8'))
 for attempt in range(2):
  try:
   FETCH_COUNT+=1
   result=json.load(urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=22));p.write_text(json.dumps(result,ensure_ascii=False),encoding='utf-8');return result
  except Exception:
   if attempt:raise
   time.sleep(20)
def clean(text):
 text=re.sub(r'<ref\b[^>]*>.*?</ref>|<ref\b[^>]*/>','',text,flags=re.S|re.I)
 for _ in range(5):text=re.sub(r'\{\{[^{}]*\}\}','',text)
 text=re.sub(r'\[\[(?:[^\]|]*\|)?([^\]]+)\]\]',r'\1',text)
 text=re.sub(r'<[^>]+>',' ',text);text=re.sub(r"'{2,}",'',text)
 return re.sub(r'\s+',' ',html.unescape(text)).strip(' *#:;|')
def norm(s):return ''.join(c for c in unicodedata.normalize('NFD',s.lower())if not unicodedata.combining(c))
def sections(w):
 matches=list(re.finditer(r'^(={2,6})\s*(.*?)\s*\1\s*$',w,re.M));out=[]
 for i,m in enumerate(matches):
  level=len(m[1]);end=len(w)
  for following in matches[i+1:]:
   if len(following[1])<=level:end=following.start();break
  out.append((clean(m[2]),w[m.end():end],level))
 return out
def parse(name,page,w,country):
 w=re.sub(r'<ref\b[^>]*>.*?</ref>|<ref\b[^>]*/>|<!--.*?-->','',w,flags=re.S|re.I)
 url='https://en.wikipedia.org/wiki/'+urllib.parse.quote(page,safe='()_')
 r={'status':'documented','founded':None,'honors':[],'players':[],'milestones':[],'sources':[{'label':'Wikipedia · '+page.replace('_',' '),'url':url}],'kits':{}}
 field=lambda key: (re.search(r'^\|\s*(?:'+key+r')\s*=\s*(.*)',w,re.M|re.I))
 found=field('founded|foundation|fundadoem|fundação|fundacao')
 if found:
  value=found[1];nums=re.findall(r'(?<!\d)(1[6-9]\d{2}|20[0-2]\d)(?!\d)',value)
  if nums:r['founded']=int(nums[0])
 for side,n in [('home',1),('away',2)]:
  k={}
  for key,inf in [('body','body'),('shorts','shorts'),('socks','socks'),('leftarm','leftarm'),('rightarm','rightarm')]:
   m=field(inf+str(n))
   if m and re.fullmatch('[0-9a-fA-F]{6}',m[1].strip()):k[key]='#'+m[1].strip().lower()
  m=field('pattern_b'+str(n))
  if m:k['patternBody']=m[1].strip()
  if 'body'in k and 'shorts'in k:r['kits'][side]=k
 for heading,content,level in sections(w):
  if re.fullmatch(r'(honours|honors|titles|achievements|palmar[eè]s|Títulos|Conquistas)',heading,re.I):
   # Retain only explicit winning rows, not runners-up, youth or women honors.
   text=content.split('==References')[0]
   text=re.split(r'^={3,}[^\n]*(?:women|feminin|youth|junior|juveni|base|under-|sub-|friendly|amistos)[^\n]*$',text,maxsplit=1,flags=re.M|re.I)[0]
   current=''
   for line in text.splitlines():
    plain=clean(line)
    if not plain:continue
    if re.search(r'(^=+.*(youth|women|reserve|friendly|under-|under |academy)|runners.?up|second place|third place|finalist|semi.final)',line,re.I):continue
    if re.search(r'\[\[.+?\]\]',line) and not re.search(r'\b(?:18|19|20)\d{2}\b',plain) and not re.search(r'(winners|champions)',plain,re.I):
     current=plain.strip(' =')
    if not re.search(r'(winner|champion|title)',plain,re.I) and not re.search(r'^\s*[;*].*\(\d+\)',line):continue
    years=re.findall(r'\b(?:18|19|20)\d{2}(?:[–-]\d{2,4})?\b',plain)
    if not years:continue
    count_match=re.search(r'(?:winners?|champions?|titles?)\s*\((\d{1,3})\)|\((\d{1,3})\)\s*:',plain,re.I)
    count=int(next(g for g in count_match.groups()if g))if count_match else None
    label=plain.split(':')[0]
    label=re.sub(r'\b(?:winners?|champions?|titles?)\b.*','',label,flags=re.I).strip(' ,;()-')
    label=re.sub(r'\s*\(\d+\)\s*','',label).strip()
    if not label or len(label)<4:label=current
    if not label or len(label)>110 or re.search(r'\d{4}',label):continue
    if label.lower()in ['domestic','international','national','regional','state','league','cup']:continue
    if any(h['name']==label for h in r['honors']):continue
    r['honors'].append({'name':label,'count':count,'years':years[:25]})
   for row in re.split(r'\n\|-',text):
    lines=[]
    for line in row.splitlines():
     if not re.match(r'^[!|]',line) or line.startswith(('{|','|}')):continue
     line=re.sub(r'\[\[(?:Ficheiro|File|Imagem|Image):.*?\]\]','',line,flags=re.I)
     line=re.sub(r'^\s*[!|]\s*(?:[^|]*[=][^|]*[|])?','',line)
     lines.extend(clean(v)for v in re.split(r'!!|\|\|',line)if clean(v))
    for j,value in enumerate(lines):
     if not re.fullmatch(r'\d{1,3}',value)or int(value)==0 or j==0 or j+1>=len(lines):continue
     label=lines[j-1]
     if re.search(r'(vice|runner|feminin|youth|juveni|junior|amistos|friendly)',label,re.I):continue
     years=re.findall(r'\b(?:18|19|20)\d{2}(?:[–-]\d{2,4})?\b',lines[j+1])
     if not years or len(label)>100 or not re.search(r'[A-Za-zÀ-ÿ]',label):continue
     if any(h['name']==label for h in r['honors']):continue
     r['honors'].append({'name':label,'count':int(value),'years':years[:25]})
   r['honors']=[t for t in r['honors'] if not re.search(r'(maior clube|ranking|seculo|século)',t['name'],re.I) and (not t.get('count') or len(t['years'])<=t['count'])][:6]
  if re.fullmatch(r'(notable (former )?players|famous players|hall of fame|club legends|historic players|Futebolistas históricos|Ídolos|Jogadores históricos|Notáveis jogadores|Jogadores notáveis|Muro dos ídolos|Maiores artilheiros|Jogadores com mais partidas|Record appearances|Record goalscorers|All-time top scorers)',heading,re.I):
   for line in content.splitlines():
    if not re.match(r'^[*#]',line):continue
    links=re.findall(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]',line)
    for target,label in links:
     p=clean(label or target)
     if ':'in target or re.search(r'(football|category|list of|[Ll]eague|[Cc]up|[Cc]hampionship|national|[Cc]lub|[Tt]eam)',p):continue
     if 3<len(p)<45 and ' 'in p and p not in r['players']:
      r['players'].append(p);break
   r['players']=[x for x in r['players'] if not re.search(r'(olympic|olimpi|summer games|football association|anos \d|série [abcd]|serie [abcd])',x,re.I) and norm(x)!=re.sub(r'-[a-z]{2}$','',norm(name))][:6]
 if not r['honors']and not r['players']:r['status']='identity-only'
 return r
PT_COUNTRY={'brazil':['brasil','brasileir'],'england':['inglaterra','ingles','gales','gales'],'usa':['estados unidos','estadunidense','americano','canada','canadense'],'spain':['espanha','espanhol'],'germany':['alemanha','alemao'],'france':['franca','frances'],'italy':['italia','italiano'],'argentina':['argentina','argentino'],'mexico':['mexico','mexicano'],'ecuador':['equador','equatoriano'],'colombia':['colombia','colombiano'],'peru':['peru','peruano'],'norway':['noruega','noruegues'],'chile':['chile','chileno'],'venezuela':['venezuela','venezuelano'],'turkey':['turquia','turco'],'netherlands':['paises baixos','holandes','neerlandes'],'uruguay':['uruguai','uruguaio'],'portugal':['portugal','portugues'],'greece':['grecia','grego'],'bolivia':['bolivia','boliviano'],'paraguay':['paraguai','paraguaio'],'belgium':['belgica','belga'],'austria':['austria','austriaco'],'ukraine':['ucrania','ucraniano'],'czech-republic':['tcheca','checa','tcheco','checo'],'azerbaijan':['azerbaijao','azerbaijano'],'slovakia':['eslovaquia','eslovaco']}
def valid_identity(name,meta,title,w,lang):
 trusted={'Santos':'Santos Futebol Clube','Botafogo':'Botafogo de Futebol e Regatas','Flamengo':'Clube de Regatas do Flamengo','Palmeiras':'Sociedade Esportiva Palmeiras','Corinthians':'Sport Club Corinthians Paulista','São Paulo':'São Paulo Futebol Clube','Vasco':'Club de Regatas Vasco da Gama','Fluminense':'Fluminense Football Club','Grêmio':'Grêmio Foot-Ball Porto Alegrense','Internacional':'Sport Club Internacional','Cruzeiro':'Cruzeiro Esporte Clube','Atlético-MG':'Clube Atlético Mineiro','Bahia':'Esporte Clube Bahia','Athletico-PR':'Club Athletico Paranaense','Coritiba':'Coritiba Foot Ball Club','Vitória':'Esporte Clube Vitória','Chapecoense':'Associação Chapecoense de Futebol','Remo':'Clube do Remo','Mirassol':'Mirassol Futebol Clube','Red Bull Bragantino':'Red Bull Bragantino','ABC':'ABC Futebol Clube'}
 if lang=='pt'and trusted.get(name)==title:return True
 # Reserves and first teams have distinct records even when they share a crest.
 if re.search(r'(?: U23| U-23| II| B| B team| Next Gen|Castilla|Fortuna|Fabril|Athletic)$',name) and not re.search(r'(U23|U-23|under.23|under.21| II| B(?:\W|$)|Next Gen|Castilla|Fortuna|Fabril|Athletic)',title,re.I):return False
 intro=re.search(r"(?m)^(?:O |A |Os |As |El |La |Il |Le )?'''",w)
 lead=norm(clean(w[intro.start():].split('\n\n',1)[0][:1000]))if intro else ''
 country=meta.get('country','')
 checks=PT_COUNTRY.get(country,[])if lang=='pt'else COUNTRIES.get(country,[country.replace('-',' ')])
 if lang=='en'and country=='usa':checks=checks+['canadian','canada']
 if lang=='en'and country=='england':checks=checks+['welsh','wales']
 return bool(checks)and any(x in lead for x in checks)
def get_team(item):
 name,meta=item;full=meta.get('name',name);country=meta.get('country','').replace('_','-')
 result={'status':'unverified','founded':None,'honors':[],'players':[],'milestones':[],'sources':[],'kits':{}}
 try:
  query=full+' '+country.replace('-',' ')+' football'
  search=req('https://en.wikipedia.org/w/rest.php/v1/search/page?'+urllib.parse.urlencode({'q':query,'limit':3}))
  pages=search.get('pages',[]);selected=None
  aliases=COUNTRIES.get(country,[country.replace('-',' ')])
  words=[x for x in re.findall('[a-z0-9]+',norm(full))if x not in ['fc','cf','sc','afc','club','clube','futebol','football','futbol','de','do','da','the','sociedade','association','calcio','sport','sporting','atletico']and len(x)>2]
  for p in pages:
   desc=norm(p.get('description',''));title=norm(p['title']);excerpt=norm(clean(p.get('excerpt','')))
   if not re.search(r'(football|soccer).*(club|team)|(club|team).*football',desc):continue
   if aliases and not any(a in desc for a in aliases):continue
   if words and sum(x in title or x in excerpt for x in words)<max(1,len(words)//2):continue
   selected=p;break
  if not selected:return name,result
  page=selected['key'];url='https://en.wikipedia.org/w/api.php?'+urllib.parse.urlencode({'origin':'*','action':'query','format':'json','titles':page,'prop':'revisions','rvprop':'content','redirects':1})
  raw=req(url);rows=list(raw['query']['pages'].values());w=rows[0]['revisions'][0]['*'];result=parse(name,rows[0]['title'].replace(' ','_'),w,country)
 except Exception as e:result['fetchError']=type(e).__name__
 return name,result

def curated_records(results):
 # Source records use explicit competition scope. They are not a grand total.
 results['Santos']={'status':'documented','founded':1912,'honors':[
  {'name':'Campeonato Brasileiro (Série A)','count':8,'years':['1961','1962','1963','1964','1965','1968','2002','2004']},
  {'name':'Copa Libertadores','count':3,'years':['1962','1963','2011']},
  {'name':'Copa Intercontinental','count':2,'years':['1962','1963']},
  {'name':'Copa do Brasil','count':1,'years':['2010']}],
 'players':['Pelé','Pepe','Coutinho','Neymar'],'milestones':['Bicampeão da Libertadores e da Copa Intercontinental em 1962 e 1963.','Tricampeonato da Libertadores conquistado em 2011.'],
 'sources':[{'label':'Santos FC · Títulos','url':'https://www.santosfc.com.br/titulos/'},{'label':'CBF · 112 anos do Santos (2024)','url':'https://www.cbf.com.br/futebol-brasileiro/noticias/campeonato-brasileiro-serie-b/a/santos-comemora-112-anos-de-historia'},{'label':'Prefeitura de Santos · História do clube','url':'https://www.santos.sp.gov.br/?q=node%2F169358'}],
 'scope':'Conquistas listadas com anos; não representa o total de troféus do clube.','kits':results.get('Santos',{}).get('kits',{})}
def main():
 data=json.loads((BASE/'app/data.json').read_text(encoding='utf-8'));logos=json.loads((BASE/'app/logos-manifest.json').read_text(encoding='utf-8'))['teams']
 teams=sorted(set(n for c in data['competitions']for n in c['teams'])-set(data['nations']))
 aliases={'Santos':'Santos Futebol Clube','Botafogo':'Botafogo de Futebol e Regatas','Flamengo':'Clube de Regatas do Flamengo','Palmeiras':'Sociedade Esportiva Palmeiras','Corinthians':'Sport Club Corinthians Paulista','São Paulo':'São Paulo Futebol Clube','Vasco':'Club de Regatas Vasco da Gama','Fluminense':'Fluminense Football Club','Grêmio':'Grêmio Foot-Ball Porto Alegrense','Internacional':'Sport Club Internacional','Cruzeiro':'Cruzeiro Esporte Clube','Atlético-MG':'Clube Atlético Mineiro','Bahia':'Esporte Clube Bahia','Athletico-PR':'Club Athletico Paranaense','Coritiba':'Coritiba Foot Ball Club','Vitória':'Esporte Clube Vitória','Chapecoense':'Associação Chapecoense de Futebol','Remo':'Clube do Remo','Mirassol':'Mirassol Futebol Clube','Red Bull Bragantino':'Red Bull Bragantino','ABC':'ABC Futebol Clube'}
 candidates={n:list(dict.fromkeys([aliases.get(n,logos.get(n,{}).get('name',n)),n]))for n in teams}
 titles=list(dict.fromkeys(t for v in candidates.values()for t in v));found={}
 for i in range(0,len(titles),35):
  part=titles[i:i+35]
  url='https://pt.wikipedia.org/w/api.php?origin=*&action=query&format=json&redirects=1&prop=revisions&rvprop=content&titles='+urllib.parse.quote('|'.join(part))
  before=FETCH_COUNT
  try:
   raw=req(url);q=raw.get('query',{});mapped={a['from']:a['to']for a in q.get('normalized',[])+q.get('redirects',[])}
   rows={p['title']:p for p in q.get('pages',{}).values()if 'revisions'in p}
   for title in part:
    target=title
    for _ in range(5):target=mapped.get(target,target)
    p=rows.get(target)
    if not p:continue
    w=p['revisions'][0]['*']
    if not re.search(r'\{\{\s*(?:Info/Clube de futebol|Info/Sport Club Corinthians Paulista|Clube de futebol|Infobox football club)',w,re.I):continue
    found[title]=(p['title'],w)
  except Exception as e:print('Batch error',i,type(e).__name__,flush=True)
  print('batch',i+len(part),'/',len(titles),'matched',len(found),flush=True)
  if FETCH_COUNT>before:time.sleep(8)
 results={}
 for n in teams:
  row=next((found[t]for t in candidates[n]if t in found and valid_identity(n,logos.get(n,{}),found[t][0],found[t][1],'pt')),None)
  if row:
   title,w=row;r=parse(n,title.replace(' ','_'),w,'');r['sources'][0]['url']=r['sources'][0]['url'].replace('en.wikipedia.org','pt.wikipedia.org')
   for side,num in [('home',1),('away',2)]:
    k=r['kits'].get(side,{})
    for key,inf in [('body','corpo'),('shorts','calções'),('socks','meias'),('leftarm','braçoesquerdo'),('rightarm','braçodireito')]:
     m=re.search(r'^\|\s*'+inf+str(num)+r'\s*=\s*([0-9a-fA-F]{6})\s*$',w,re.M)
     if m:k[key]='#'+m[1].lower()
    if 'body'in k and 'shorts'in k:r['kits'][side]=k
   results[n]=r
  else:results[n]={'status':'unverified','founded':None,'honors':[],'players':[],'milestones':[],'sources':[],'kits':{}}
 curated_records(results)
 coverage={'clubs':len(teams),'documented':sum(v['status']=='documented'for v in results.values()),'foundation':sum(bool(v.get('founded'))for v in results.values()),'honors':sum(bool(v.get('honors'))for v in results.values()),'players':sum(bool(v.get('players'))for v in results.values()),'homeAwayKits':sum('home'in v.get('kits',{})and 'away'in v.get('kits',{})for v in results.values()),'unverified':sum(v['status']=='unverified'for v in results.values())}
 archive={'updatedAt':'2026-10-27','note':'Dados históricos por fonte; contagens por competição, não total de títulos. Campos vazios não significam zero.','coverage':coverage,'teams':results}
 (BASE/'app/club-history.json').write_text(json.dumps(archive,ensure_ascii=False,indent=2),encoding='utf-8');(BASE/'app/club-history.js').write_text('window.PP_CLUB_HISTORY='+json.dumps(archive,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8');print(json.dumps(coverage),flush=True)
def enrich_english():
 path=BASE/'app/club-history.json';archive=json.loads(path.read_text(encoding='utf-8'));results=archive['teams'];logos=json.loads((BASE/'app/logos-manifest.json').read_text(encoding='utf-8'))['teams']
 candidates={n:list(dict.fromkeys([logos.get(n,{}).get('name',n),n,n+' FC',n+' F.C.']))for n,r in results.items()if r['status']=='unverified'}
 titles=list(dict.fromkeys(t for names in candidates.values()for t in names));found={}
 if '--cached' in __import__('sys').argv:
  rows={};redirects={}
  for cache in CACHE.glob('*.json'):
   q=json.loads(cache.read_text(encoding='utf-8')).get('query',{})
   redirects.update({r['from']:r['to']for r in q.get('normalized',[])+q.get('redirects',[])})
   for row in q.get('pages',{}).values():
    if row.get('revisions'):
     w=row['revisions'][0]['*']
     if re.search(r'\{\{\s*Infobox football club',w,re.I):rows[row['title']]=w
  for title in titles:
   target=title
   for _ in range(6):target=redirects.get(target,target)
   if target in rows:found[title]=(target,rows[target])
 for i in range(0,0 if '--cached' in __import__('sys').argv else len(titles),50):
  part=titles[i:i+50];before=FETCH_COUNT
  url='https://en.wikipedia.org/w/api.php?origin=*&action=query&format=json&redirects=1&prop=revisions&rvprop=content&titles='+urllib.parse.quote('|'.join(part))
  try:
   raw=req(url);q=raw.get('query',{});mapped={a['from']:a['to']for a in q.get('normalized',[])+q.get('redirects',[])};rows={p['title']:p for p in q.get('pages',{}).values()if 'revisions'in p}
   for title in part:
    target=title
    for _ in range(5):target=mapped.get(target,target)
    page=rows.get(target)
    if not page:continue
    w=page['revisions'][0]['*']
    if re.search(r'\{\{\s*Infobox football club',w,re.I):found[title]=(page['title'],w)
  except Exception as e:print('EN batch error',i,type(e).__name__,flush=True)
  print('EN',i+len(part),'/',len(titles),'articles',len(found),flush=True)
  if FETCH_COUNT>before:time.sleep(8)
 for name,names in candidates.items():
  row=next((found[t]for t in names if t in found and valid_identity(name,logos.get(name,{}),found[t][0],found[t][1],'en')),None)
  if row:results[name]=parse(name,row[0].replace(' ','_'),row[1],logos.get(name,{}).get('country',''))
 # Two homonymous Brazilian/Spanish clubs must never share the Athletic record.
 if 'Athletic Club'in results:
  src=' '.join(x['url']for x in results['Athletic Club']['sources'])
  if 'Athletic_Club'in src and not re.search('Minas|Brazil|Brasil',src,re.I):results['Athletic Club']={'status':'unverified','founded':None,'honors':[],'players':[],'milestones':[],'sources':[],'kits':{}}
 curated_records(results)
 archive['coverage']={'clubs':len(results),'documented':sum(v['status']=='documented'for v in results.values()),'foundation':sum(bool(v.get('founded'))for v in results.values()),'honors':sum(bool(v.get('honors'))for v in results.values()),'players':sum(bool(v.get('players'))for v in results.values()),'homeAwayKits':sum('home'in v.get('kits',{})and 'away'in v.get('kits',{})for v in results.values()),'unverified':sum(v['status']=='unverified'for v in results.values())}
 path.write_text(json.dumps(archive,ensure_ascii=False,indent=2),encoding='utf-8');(BASE/'app/club-history.js').write_text('window.PP_CLUB_HISTORY='+json.dumps(archive,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8');print(json.dumps(archive['coverage']),flush=True)
if __name__=='__main__':
 import sys
 if '--english'in sys.argv:enrich_english()
 else:main()
