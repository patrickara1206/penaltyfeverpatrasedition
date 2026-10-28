from pathlib import Path
import importlib.util,json,re,urllib.parse,time
base=Path(__file__).resolve().parents[1];spec=importlib.util.spec_from_file_location('hist',base/'tools/build_club_history.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
archive=json.loads((base/'app/club-history.json').read_text(encoding='utf-8'));bytitle={}
for f in h.CACHE.glob('*.json'):
 raw=json.loads(f.read_text(encoding='utf-8'))
 for row in raw.get('query',{}).get('pages',{}).values():
  if row.get('revisions'):bytitle[row['title']]=row['revisions'][0]['*']
needs={}
for name,record in archive['teams'].items():
 if record['honors']:continue
 src=next((x['url']for x in record['sources']if 'pt.wikipedia.org/wiki/'in x['url']),None)
 if not src:continue
 title=urllib.parse.unquote(src.split('/wiki/')[1]).replace('_',' ');w=bytitle.get(title,'')
 for heading,body,level in h.sections(w):
  if heading.lower()not in ['títulos','conquistas']:continue
  refs=re.findall(r'\{\{\s*((?:Títulos|Troféus|Palmarés)[^{}|\n]*)\s*(?:\||\}\})',body,re.I)
  refs=['Predefinição:'+x.strip()for x in refs]
  if refs:needs[name]=refs[:2]
titles=list(dict.fromkeys(t for refs in needs.values()for t in refs));fetched={t:bytitle[t] for t in titles if t in bytitle};titles=[t for t in titles if t not in fetched]
print('Missing honors with title templates:',len(needs),'templates:',len(titles),flush=True)
for i in range(0,len(titles),30):
 part=titles[i:i+30];url='https://pt.wikipedia.org/w/api.php?origin=*&action=query&format=json&redirects=1&prop=revisions&rvprop=content&titles='+urllib.parse.quote('|'.join(part));raw=h.req(url);q=raw.get('query',{});redirect={x['from']:x['to']for x in q.get('normalized',[])+q.get('redirects',[])};rows={p['title']:p for p in q.get('pages',{}).values()if p.get('revisions')}
 for t in part:
  dest=redirect.get(t,t)
  if dest in rows:fetched[t]=rows[dest]['revisions'][0]['*']
 print('templates',i+len(part),'/',len(titles),flush=True)
changed=[]
for name,refs in needs.items():
 for title in refs:
  if title not in fetched:continue
  r=h.parse(name,title,'== Títulos ==\n'+fetched[title],'')
  if not r['honors']:continue
  record=archive['teams'][name];record['honors']=r['honors'];record['status']='documented';record['sources'].append({'label':'Wikipedia · quadro de títulos','url':'https://pt.wikipedia.org/wiki/'+urllib.parse.quote(title.replace(' ','_'))});changed.append(name);break
h.curated_records(archive['teams']);r=archive['teams'];archive['coverage']={'clubs':len(r),'documented':sum(x['status']=='documented'for x in r.values()),'foundation':sum(bool(x.get('founded'))for x in r.values()),'honors':sum(bool(x.get('honors'))for x in r.values()),'players':sum(bool(x.get('players'))for x in r.values()),'homeAwayKits':sum('home'in x.get('kits',{})and 'away'in x.get('kits',{})for x in r.values()),'unverified':sum(x['status']=='unverified'for x in r.values())};archive['updatedAt']='2026-10-28'
(base/'app/club-history.json').write_text(json.dumps(archive,ensure_ascii=False,indent=2),encoding='utf-8');(base/'app/club-history.js').write_text('window.PP_CLUB_HISTORY='+json.dumps(archive,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8');print(json.dumps({'enriched':changed,'coverage':archive['coverage']},ensure_ascii=True),flush=True)
