'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const base=path.join(__dirname,'..'),app=path.join(base,'app');
const F=require(path.join(app,'football.js'));
const sandbox={window:{},Uint8Array,atob};vm.createContext(sandbox);vm.runInContext(fs.readFileSync(path.join(app,'data.js'),'utf8'),sandbox);
const source=fs.readFileSync(path.join(app,'app.js'),'utf8'),start=source.indexOf('function kitPreset('),end=source.indexOf('\nfunction kit(',start);
assert(start>=0&&end>start);
const history=JSON.parse(fs.readFileSync(path.join(app,'club-history.json'),'utf8'));
const kitPreset=new Function('F','baseKits','window','return ('+source.slice(start,end)+')')(F,sandbox.window.PP_KITS,{PP_CLUB_HISTORY:history});
const teams=[...new Set(sandbox.window.PP_DATA.competitions.flatMap(c=>c.teams).concat(sandbox.window.PP_DATA.nations))];
for(const n of teams)for(const variant of ['home','away']){
 const k=kitPreset(n,variant);for(const key of ['a','b','shorts','number'])assert.match(k[key],/^#[a-f0-9]{6}$/i,n+' '+variant+' '+key);
 assert([0,1,2,3,4,5].includes(k.pattern),n+' '+variant);assert(typeof F.css(k)==='string');
}
const clubs=teams.filter(n=>!sandbox.window.PP_DATA.nations.includes(n));
for(const n of clubs){
 const h=history.teams[n];assert(h,n);assert(Array.isArray(h.honors)&&Array.isArray(h.players)&&Array.isArray(h.sources),n);
 if(h.founded)assert(Number(h.founded)>=1600&&Number(h.founded)<=2026,n);
 if(h.honors.length||h.players.length)assert(h.sources.length,n+' missing source');
 for(const t of h.honors){assert(t.name&&typeof t.name==='string',n);assert(t.count==null||(Number.isInteger(t.count)&&t.count>0&&t.count<500),n+' count');}
 for(const s of h.sources)assert.match(s.url,/^https:\/\//,n+' source');
}
const html=fs.readFileSync(path.join(app,'index.html'),'utf8');assert(html.includes('src="club-history.js"'));assert(!html.includes('type="color"'));assert(html.includes('id="brandHome"'));
const report={status:'passed',presetTeams:teams.length,presetChoices:teams.length*2,clubRecords:clubs.length,historyCoverage:history.coverage};
fs.writeFileSync(path.join(base,'VALIDACAO-EDICAO.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
