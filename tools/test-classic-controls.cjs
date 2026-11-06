"use strict";
const fs=require('node:fs'),cp=require('node:child_process'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const baseline=cp.execFileSync('git',['show','c82ee75:app/match.swf'],{cwd:__dirname+'/..',maxBuffer:20*1024*1024});
const current=fs.readFileSync(__dirname+'/../app/match.swf');
const zlib=require('node:zlib');function tags(raw){const d=zlib.inflateSync(raw.subarray(8));let p=Math.ceil((5+4*(d[0]>>3))/8)+4,f=0;const out=[];while(p<d.length){const begin=p,h=d.readUInt16LE(p);p+=2;let n=h&63,t=h>>6;if(n===63){n=d.readUInt32LE(p);p+=4}p+=n;out.push({t,f,b:d.subarray(begin,p)});if(t===1)f++;if(!t)break}return out}const before=tags(baseline),after=tags(current);assert.equal(after.length,before.length);for(let i=0;i<before.length;i++){const a=before[i],b=after[i];assert.equal(a.t,b.t);assert.equal(a.f,b.f);if(a.t===12&&[75,101].includes(a.f))continue;assert.deepEqual(b.b,a.b,'Changed v1.0.6 animation or physics at tag '+i+' frame '+a.f)}
// Native actions remain exact even in the frame with the cosmetic number hook.
assert.deepEqual(after.find(x=>x.t===12&&x.f===101).b,before.find(x=>x.t===12&&x.f===101).b);
for(const path of ['app/runtime-config.js','app/football.js'])assert.equal(fs.readFileSync(__dirname+'/../'+path,'utf8').replaceAll('\r\n','\n'),cp.execFileSync('git',['show','c82ee75:'+path],{cwd:__dirname+'/..',encoding:'utf8'}).replaceAll('\r\n','\n'),'Changed runtime or difficulty: '+path);
const js=fs.readFileSync(__dirname+'/../app/app.js','utf8'),old=cp.execFileSync('git',['show','c82ee75:app/app.js'],{cwd:__dirname+'/..',encoding:'utf8'});
const params=s=>s.slice(s.indexOf('const params='),s.indexOf(';paramKit',s.indexOf('const params=')));
assert.equal(params(js),params(old),'Launcher parameters differ from v1.0.6');
console.log('PASS: v1.0.6 physics and actor timelines identical; only display initialization and cosmetic number hook differ; same runtime configuration, difficulty and launcher controls. SHA256 '+crypto.createHash('sha256').update(current).digest('hex'));

const src=fs.readFileSync(__dirname+'/build_match.py','utf8'),oldSrc=cp.execFileSync('git',['show','c82ee75:tools/build_match.py'],{cwd:__dirname+'/..',encoding:'utf8'});const hooks=s=>s.slice(s.indexOf("# A shooter's setup"),s.indexOf('for f in [102')).replaceAll('\r\n','\n');assert.equal(hooks(src),hooks(oldSrc),'Physics setup hooks differ from v1.0.6');
