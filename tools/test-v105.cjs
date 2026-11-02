'use strict';
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert/strict'),crypto=require('crypto');
const app=path.join(__dirname,'../app'),read=f=>fs.readFileSync(path.join(app,f),'utf8');
// Goal geometry moved to the swept-plane regression suite in v1.0.6.
require('./test-v106.cjs');
// Portable WebAssembly fragments reconstruct valid unchanged WASM modules.
const c={window:{}};vm.createContext(c);for(const file of fs.readdirSync(path.join(app,'runtime')).sort())vm.runInContext(read('runtime/'+file),c);assert.equal(Object.keys(c.window.PF_WASM_ASSETS).length,2);for(const b64 of Object.values(c.window.PF_WASM_ASSETS)){const b=Buffer.from(b64,'base64');assert.equal(b.subarray(0,4).toString('hex'),'0061736d');assert(WebAssembly.validate(b));}
assert(read('index.html').includes('settings.js'));assert(read('features-v104.js').includes('api.enterFullscreen()'));assert(!read('quick-select.js').includes('EXIBIÇÃO <b>VS'));
const settings=read('settings.js');assert(settings.includes('protanopia')&&settings.includes('deuteranopia')&&settings.includes('tritanopia'));assert(settings.includes('prefs.scale=parseInt'));
const labels=JSON.parse(fs.readFileSync(path.join(__dirname,'actionscript/text-labels.json'),'utf8'));assert.equal(labels.length,30);for(const lang of ['pt','en','es','fr','de','it','zh','ar','hi','ru'])assert.equal(labels.filter(x=>x.language===lang).length,3);for(const row of labels)assert(row.width>0&&row.height>0&&row.text.length>0);
console.log('PASS v1.0.5: swept goal geometry; 2 real WASM modules; Ruffle fullscreen; settings; quick match label');

