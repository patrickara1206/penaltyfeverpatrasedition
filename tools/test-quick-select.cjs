'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),Q=require('../app/quick-select.js');
const d=JSON.parse(fs.readFileSync(path.join(__dirname,'../app/data.json'),'utf8'));
const brazil=Q.list(d,'current','Brasil','br0');assert.equal(brazil.length,20);assert(brazil.includes('Flamengo'));assert(!brazil.includes('Real Madrid'));
assert(Q.list(d,'current','Brasil','all','sao paulo').includes('São Paulo'));assert.equal(Q.list(d,'current','Brasil','all','not-a-club').length,0);
assert.equal(Q.step(0,-1,20),19);assert.equal(Q.step(19,1,20),0);assert.equal(Q.step(0,1,0),-1);
for(const n of [0,1,2,3,4,5,20,872])for(let i=0;i<Math.max(n,1);i++){const slots=Q.slots(i,n);assert.equal(slots.length,Math.min(n,5));assert.equal(new Set(slots.map(x=>x.index)).size,slots.length);if(n)assert.equal(slots.find(x=>x.offset===0).index,i);}
const current=Q.list(d,'current');assert.equal(current.length,new Set(d.competitions.filter(c=>!c.historical).flatMap(c=>c.teams)).size);assert.equal(Q.list(d,'archive').length,new Set(d.archive).size);
for(const c of d.competitions.filter(c=>!c.historical))assert.equal(Q.list(d,'current',Q.country(c),c.id).length,new Set(c.teams).size,c.id);
console.log(JSON.stringify({status:'passed',competitions:d.competitions.length,currentTeams:current.length,checks:['filters and accent-insensitive search','wrap-around','zero and small lists','all competitions reachable','classic archive retained']},null,2));
