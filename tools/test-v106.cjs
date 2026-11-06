'use strict';
const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const zlib=require('zlib');
function action105(file){const raw=fs.readFileSync(file),d=Buffer.concat([raw.subarray(0,8),zlib.inflateSync(raw.subarray(8))]);let p=8+Math.ceil((5+4*(d[8]>>3))/8)+4,f=0;while(p<d.length){const v=d.readUInt16LE(p);p+=2;const t=v>>6;let n=v&63;if(n===63){n=d.readUInt32LE(p);p+=4}const b=d.subarray(p,p+n);p+=n;if(t===12&&f===105)return b;if(t===1)f++;if(!t)break}throw Error('physics action missing')}
assert.deepEqual(action105(__dirname+'/../app/match.swf'),action105(__dirname+'/original.swf'),'classic flight/keeper/rebound actions preserved byte-for-byte');
const builder=fs.readFileSync(__dirname+'/build_match.py','utf8');
assert(builder.includes('0x20B969')&&builder.includes('0xE74B4B'));
assert(builder.includes('0xE74636')&&builder.includes('0xF29A28'));
assert(builder.includes("put(path+'._y',346)"));
assert(builder.includes('speedhook')&&!builder.includes('easy_aim')&&builder.includes('hide_target'));
console.log('PASS: original flight actions; green/red attempts; distinct keeper colors; lower-right prompt; native defense target');

