'use strict';
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert/strict'),crypto=require('crypto');
const app=path.join(__dirname,'../app'),read=f=>fs.readFileSync(path.join(app,f),'utf8');
// Execute the complete real AS2 goal decision branch as equivalent JS with movie/audio stubs.
const source=fs.readFileSync(path.join(__dirname,'actionscript/physics.as'),'utf8');
const begin=source.indexOf('dLoptaOsaGola ='),end=source.indexOf('\nif(gol)',begin);
assert(begin>=0&&end>begin);const code=source.slice(begin,end).replace(/\band\b/g,'&&').replace(/\bor\b/g,'||');
const clip=()=>({swapDepths(){},start(){},setVolume(){}});
function goal(x,y,{held=false,dy=-12,shadowX=305}={}){const c={Math,osaGola:305,xSenka:shadowX,senka:{_x:shadowX,_y:168},lopta:{_x:x,_y:y,_width:8,_height:8},golLinija:168,gol:false,uGolu:false,uRuci:held,dey:dy,dex:0,visinaGola:80,sirinaGola:240,sabirak:168-y,fiGola:6,pocbrzina:12,ugaokretanjarad:Math.PI,maksvisina:45,rezBrzina:12,pocetni_ugao:0,omega:0.05,brojac:0};for(const n of ['golmance','gol_senka','okvirGola','mrezaGornja','zvukGol','zvukStativa','zvukPromasaj'])c[n]=clip();vm.runInNewContext(code,c);return c.gol;}
assert.equal(goal(305,140),true,'normal goal');assert.equal(goal(305,168),true,'ground goal');assert.equal(goal(450,140),false,'ball wide, shadow central');assert.equal(goal(160,140),false,'ball wide left');assert.equal(goal(305,80),false,'ball over crossbar');assert.equal(goal(305,140,{held:true}),false,'catch is not goal');assert.equal(goal(305,140,{dy:12}),false,'outbound ball is not goal');assert.equal(goal(305,140,{shadowX:500}),true,'ball controls horizontal decision');
// Portable WebAssembly fragments reconstruct valid unchanged WASM modules.
const c={window:{}};vm.createContext(c);for(const file of fs.readdirSync(path.join(app,'runtime')).sort())vm.runInContext(read('runtime/'+file),c);assert.equal(Object.keys(c.window.PF_WASM_ASSETS).length,2);for(const b64 of Object.values(c.window.PF_WASM_ASSETS)){const b=Buffer.from(b64,'base64');assert.equal(b.subarray(0,4).toString('hex'),'0061736d');assert(WebAssembly.validate(b));}
assert(read('index.html').includes('settings.js'));assert(read('features-v104.js').includes('api.enterFullscreen()'));assert(!read('quick-select.js').includes('EXIBIÇÃO <b>VS'));
const settings=read('settings.js');assert(settings.includes('protanopia')&&settings.includes('deuteranopia')&&settings.includes('tritanopia'));assert(settings.includes('prefs.scale=parseInt'));
const labels=JSON.parse(fs.readFileSync(path.join(__dirname,'actionscript/text-labels.json'),'utf8'));assert.equal(labels.length,30);for(const lang of ['pt','en','es','fr','de','it','zh','ar','hi','ru'])assert.equal(labels.filter(x=>x.language===lang).length,3);for(const row of labels)assert(row.width>0&&row.height>0&&row.text.length>0);
console.log('PASS v1.0.5: 8 goal geometry cases; 2 real WASM modules; Ruffle fullscreen; settings; quick match label');

