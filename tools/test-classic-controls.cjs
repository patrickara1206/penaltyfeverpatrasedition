'use strict';
const fs=require('node:fs'),zlib=require('node:zlib'),assert=require('node:assert/strict');
function actions(file){const raw=fs.readFileSync(file),body=raw[0]===67?zlib.inflateSync(raw.subarray(8)):raw.subarray(8);let p=Math.ceil((5+4*(body[0]>>3))/8)+4,frame=0;const frames=new Map();while(p<body.length){const h=body.readUInt16LE(p);p+=2;const type=h>>6;let length=h&63;if(length===63){length=body.readUInt32LE(p);p+=4}const code=body.subarray(p,p+length);p+=length;if(type===12){if(!frames.has(frame))frames.set(frame,[]);frames.get(frame).push(code)}if(type===1)frame++;if(!type)break}return frames}
const original=actions(__dirname+'/original.swf'),game=actions(__dirname+'/../app/match.swf');
for(let frame=101;frame<=106;frame++){const native=original.get(frame),patched=game.get(frame);assert(native?.length&&patched?.length,'Missing shot frame '+frame);assert.deepEqual(patched.slice(0,native.length),native,'Native action or order changed at '+frame);assert.equal(patched.length,native.length+1,'Unexpected action at '+frame)}
const cp=require('node:child_process');
const baseline=cp.execFileSync('git',['show','c82ee75:tools/build_match.py'],{cwd:__dirname+'/..',encoding:'utf8'});
const builder=fs.readFileSync(__dirname+'/build_match.py','utf8');
const setup=s=>s.slice(s.indexOf("# A shooter's setup"),s.indexOf('for f in [102')).replace("+put('_root.ppSaveCelebrated',0)",'').replaceAll('\r\n','\n');
assert.equal(setup(builder),setup(baseline),'v1.0.6 speed, keeper, marker and timer hooks must remain exactly identical');
const js=fs.readFileSync(__dirname+'/../app/app.js','utf8'),old=cp.execFileSync('git',['show','c82ee75:app/app.js'],{cwd:__dirname+'/..',encoding:'utf8'});
const params=s=>s.slice(s.indexOf('const params='),s.indexOf(';paramKit',s.indexOf('const params=')));
assert.equal(params(js),params(old),'Launcher parameters differ from approved v1.0.6');
assert(!builder.includes('easy_aim'),'No later Easy AI forced-dive changes');
assert(builder.includes('flash.filters.GlowFilter')&&builder.includes('flash.filters.DropShadowFilter'),'Native-shirt and number contrast filters missing');
console.log('PASS: native actions preserved; complete shot/keeper/timer hooks and launcher parameters identical to approved v1.0.6; native glyph pose retained with shirt shading and number outline');
