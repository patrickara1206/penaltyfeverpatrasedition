'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const root=path.join(__dirname,'..'),S=require('../app/security.js'),L=require('../app/lz-string.min.js'),Storage=require('../app/storage.js');
let checks=0;const reject=fn=>{assert.throws(fn);checks++};
for(const payload of ['{"__proto__":{"polluted":true}}','{"x":{"constructor":{"prototype":{"polluted":true}}}}','{"x":{"prototype":{"x":1}}}'])reject(()=>S.parseJSON(payload));
assert.equal({}.polluted,undefined);checks++;
let deep={};for(let i=0;i<70;i++)deep={n:deep};reject(()=>S.parseJSON(JSON.stringify(deep)));
reject(()=>S.inspect({x:'x'.repeat(2000001)}));reject(()=>S.parseJSON('{broken'));reject(()=>Storage.decode('PFZ3:invalid'));
const normal={version:3,campaigns:{},kits:{},careers:{},text:'Ação · São Paulo <img src=x onerror=alert(1)>'};assert.deepEqual(Storage.decode(Storage.encode(normal)),normal);checks++;
const compressed=L.compressToUTF16('a'.repeat(100000));reject(()=>L.decompressFromUTF16(compressed,1000));assert.equal(L.decompressFromUTF16(compressed,100000).length,100000);checks++;
for(const bad of ['javascript:alert(1)','data:text/html,evil','http://example.org/','file:///C:/secret']){assert.equal(S.safeURL(bad),'#');checks++;}
assert.equal(S.safeURL('https://www.santosfc.com.br/titulos/'),'https://www.santosfc.com.br/titulos/');checks++;
const html=fs.readFileSync(path.join(root,'app/index.html'),'utf8');assert(!/<script(?![^>]*\bsrc=)[^>]*>\s*\S/i.test(html));checks++;
assert(html.includes("script-src 'self' 'wasm-unsafe-eval'")&&!html.includes("'unsafe-eval'"));checks++;
for(const rule of ["object-src 'none'","base-uri 'none'","form-action 'none'","connect-src 'none'"]){assert(html.includes(rule));checks++;}
const js=fs.readFileSync(path.join(root,'app/app.js'),'utf8');assert(!/onclick="/.test(js));assert(js.includes('PFSecurity.parseJSON(await f.text())'));checks++;
const report={status:'passed',checks,scope:['prototype keys','depth and text limits','bounded LZ expansion','valid compressed save roundtrip','external URL schemes','CSP and inline handlers'],limits:['client-side controls are not anti-cheat or a guarantee of invulnerability','no backend or shared leaderboard exists']};fs.writeFileSync(path.join(root,'VALIDACAO-SEGURANCA.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
