'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.join(__dirname,'..');
// Execute the actual patched vendor bridge with dynamic code generation disabled (CSP equivalent).
for(const file of fs.readdirSync(path.join(root,'app')).filter(x=>/^core\.ruffle\..*\.js$/.test(x))){
 const src=fs.readFileSync(path.join(root,'app',file),'utf8'),bridge=src.match(/function r\(e,_\)\{if\(!\[.*?return n\(\.\.\._\)\}/)[0],calls=[];
 const window={};for(const name of ['patrasReady','patrasTurn','patrasShot','patrasProgress','patrasResult'])window[name]=(...args)=>calls.push({name,args});
 const c=vm.createContext({window},{codeGeneration:{strings:false,wasm:false}});vm.runInContext(bridge,c);
 for(const name of Object.keys(window))c.r(name,[5,3]);assert.equal(calls.length,5);assert.equal(calls[4].name,'patrasResult');assert.deepEqual(calls[4].args,[5,3]);
 for(const payload of ['alert','window.patrasResult','(()=>alert(1))','constructor','__proto__'])assert.throws(()=>c.r(payload,[]),/denied/);
}
// Exercise real application launch/result handlers with only the browser DOM/runtime stubbed.
const elements=new Map();const el=id=>{if(!elements.has(id)){const classes=new Set(['hide']);elements.set(id,{textContent:'',dataset:{},classList:{add:x=>classes.add(x),remove:x=>classes.delete(x),toggle:(x,b)=>b?classes.add(x):classes.delete(x),contains:x=>classes.has(x)},showModal(){this.open=true},close(){this.open=false},setAttribute(){},replaceChildren(){},append(){}})}return elements.get(id)};
const E=require('../app/engine.js'),F=require('../app/football.js'),C=require('../app/career.js'),data=JSON.parse(fs.readFileSync(path.join(root,'app/data.json'),'utf8'));
const timers=[],c=vm.createContext({console,PatrasEngine:E,PFFootball:F,PFCareer:C,document:{getElementById:el,querySelectorAll:()=>[]},window:{scrollTo(){}},localStorage:{setItem(){}},PFStorage:{encode:JSON.stringify},setTimeout:fn=>timers.push(fn),clearTimeout(){}});
vm.runInContext(fs.readFileSync(path.join(root,'app/features-v104.js'),'utf8'),c);
const app=fs.readFileSync(path.join(root,'app/app.js'),'utf8').replace(/boot\(\);\s*$/,'');vm.runInContext(app,c);c.fixtureData=data;
vm.runInContext("data=fixtureData;season=E.create(data.competitions.find(x=>x.id==='br0'),'Santos',3);startMatch=i=>{window.launched=i};launchSeason()",c);
assert.equal(c.window.launched.kind,'season');assert.equal(c.window.launched.user,'Santos');assert.equal(c.window.launched.draw,true);assert(c.window.launched.m);
vm.runInContext("pending={kind:'quick',home:'Flamengo',away:'Palmeiras',user:'Flamengo'};renderQuick=()=>{window.returned=true}",c);
c.window.patrasResult(5,3);c.window.patrasResult(5,3);assert.equal(timers.length,1);timers.shift()();
assert.equal(el('resultOverlay').classList.contains('hide'),false);assert.equal(el('resultScore').textContent,'5 × 3');assert.equal(vm.runInContext('store.quickHistory.length',c),1);assert.equal(vm.runInContext('store.activeMatch',c),null);el('continue').onclick();assert(c.window.returned);assert.equal(el('resultOverlay').classList.contains('hide'),true);
vm.runInContext("store.campaigns=Object.fromEntries(Array.from({length:12},(_,i)=>['c'+i,{id:i}]));store.careers=Object.fromEntries(Array.from({length:7},(_,i)=>['k'+i,{id:i}]));store.quickHistory=Array.from({length:7},(_,i)=>({id:i}));limitSavedRecords()",c);
assert.equal(vm.runInContext('Object.keys(store.campaigns).length',c),10);assert.equal(vm.runInContext('Object.keys(store.campaigns)[0]',c),'c2');assert.equal(vm.runInContext('Object.keys(store.careers)[0]',c),'k2');assert.equal(vm.runInContext('store.quickHistory[0].id',c),2);
vm.runInContext("window.moved=false;confirmCareerYear({year:2035,history:[{year:2026}]},()=>{window.moved=true})",c);assert.equal(c.window.moved,false);assert(el('historyWarning').open);el('historyWarningConfirm').onclick();assert(c.window.moved);assert.equal(el('historyWarning').open,false);
console.log('PASS: season launch, quick result/history/return, duplicate callback, both Ruffle bridges under CSP, rejected arbitrary callbacks, FIFO caps, history warning before rollover');

