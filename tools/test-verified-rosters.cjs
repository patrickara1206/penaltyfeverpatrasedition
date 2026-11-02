'use strict';
const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const context={};context.window=context;vm.createContext(context);
for(const file of ['rosters-verified.js','football.js'])vm.runInContext(fs.readFileSync(__dirname+'/../app/'+file,'utf8'),context);
const data=JSON.parse(fs.readFileSync(__dirname+'/../app/rosters-verified.json','utf8'));
assert.deepEqual(JSON.parse(JSON.stringify(context.PF_VERIFIED_ROSTERS)),data);
let total=0;for(const [club,record]of Object.entries(data.clubs)){
 assert(record.source.startsWith('https://'));assert.equal(record.consultedAt,'2026-11-02');assert.match(record.sourceSha256,/^[0-9a-f]{64}$/);
 assert(record.players.length>=11);assert.equal(new Set(record.players.map(x=>x.name)).size,record.players.length);
 for(const p of record.players){assert(p.confirmed);assert(p.name&&!p.name.includes('\ufffd'));assert(p.number===null||Number.isInteger(p.number));}
 const info=context.PFFootball.rosterInfo(club),r=context.PFFootball.roster(club);
 assert(info.confirmed);assert.equal(r[0].role,'Goleiro');assert(r.slice(1).every(p=>p.role!=='Goleiro'&&p.confirmed));
 assert(r.slice(1).every(p=>record.players.some(q=>q.name===p.name)));total+=record.players.length;
}
assert(!context.PFFootball.rosterInfo('Clube sem fonte').confirmed);
assert.equal(context.PFFootball.roster('Clube sem fonte').length,11);
assert(fs.readFileSync(__dirname+'/../app/index.html','utf8').indexOf('rosters-verified.js')<fs.readFileSync(__dirname+'/../app/index.html','utf8').indexOf('football.js'));
console.log('PASS: '+Object.keys(data.clubs).length+' sourced club rosters, '+total+' named players, goalkeeper exclusion, unknown numbers preserved, fictional fallback labelled');
