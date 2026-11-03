'use strict';
const fs=require('fs'),zlib=require('zlib'),assert=require('assert/strict');
const raw=fs.readFileSync(__dirname+'/../app/match.swf'),swf=zlib.inflateSync(raw.subarray(8));
const marker=Buffer.from('_root.ppAnimateStadium\0'),at=swf.indexOf(marker)+marker.length;assert(at>=marker.length&&swf[at]===0x9b);
const code=swf.subarray(at+8,at+8+swf.readUInt16LE(at+6));
// Execute the actual generated AS2 animation function, including its string flag.
function run(now,{reduce='0',home=0,away=0}={}){const vars={'Math':Math,'_root.ppHomeCheerUntil':home,'_root.ppAwayCheerUntil':away,'_root.pp_reduce_motion':reduce,'_root.ppSponsors':Array.from({length:12},(_,i)=>'brand'+i),'_root.ppSlogans':Array.from({length:12},(_,i)=>'line'+i)},stack=[];let p=0,steps=0;
 while(p<code.length&&steps++<100000){const op=code[p++];if(!op)break;let n=0;if(op>=128){n=code.readUInt16LE(p);p+=2}const end=p+n;
 if(op===0x96){while(p<end){const type=code[p++];if(type===0){const z=code.indexOf(0,p);stack.push(code.toString('utf8',p,z));p=z+1}else if(type===7){stack.push(code.readInt32LE(p));p+=4}else if(type===1){stack.push(code.readFloatLE(p));p+=4}else throw Error('Push type '+type)}}
 else if(op===0x1c)stack.push(vars[stack.pop()]);
 else if(op===0x1d){const value=stack.pop(),name=stack.pop();vars[name]=value}
 else if(op===0x34)stack.push(now);
 else if(op===0x12)stack.push(!stack.pop());
 else if(op===0x9d){const jump=code.readInt16LE(p);p=end;if(stack.pop())p+=jump;continue}
 else if(op===0x52){const method=stack.pop(),object=stack.pop(),count=stack.pop(),args=[];for(let i=0;i<count;i++)args.push(stack.pop());stack.push(object[method](...args))}
 else if(op===0x4e){const key=stack.pop(),object=stack.pop();stack.push(object[key])}
 else if([0x0b,0x0c,0x0d,0x3f,0x47,0x49].includes(op)){const b=stack.pop(),a=stack.pop();stack.push(op===0x0b?a-b:op===0x0c?a*b:op===0x0d?a/b:op===0x3f?a%b:op===0x47?a+b:a==b)}
 else throw Error('Unexpected animation opcode '+op.toString(16));
 p=end;
 }assert(steps<100000);return vars;}
const idle=run(10000),later=run(10500),home=run(10000,{home:13000}),away=run(10000,{away:13000});
assert(Math.abs(home['_root.ppCheerHome']-3)<1e-5);assert.equal(home['_root.ppCheerAway'],0);assert.equal(away['_root.ppCheerHome'],0);assert(Math.abs(away['_root.ppCheerAway']-3)<1e-5);
const fans=Object.keys(idle).filter(k=>k.includes('.ppFan')&&k.endsWith('._y'));assert(fans.length>=20&&fans.length<60);assert(fans.some(k=>Math.abs(idle[k]-later[k])>.1),'crowd moves with string 0');assert(fans.some(k=>Math.abs(idle[k]-home[k])>2),'home celebration');assert(fans.some(k=>Math.abs(idle[k]-away[k])>2),'away celebration');
const still=run(10000,{reduce:'1',home:13000}),stillLater=run(10500,{reduce:'1',home:13000});for(const k of fans)assert.equal(still[k],stillLater[k]);
assert(run(5000)['_root.ppBrand.ppAdRibbon._x']<0);assert.notEqual(run(5000)['_root.ppBrand.ppAdRibbon._x'],run(25000)['_root.ppBrand.ppAdRibbon._x']);assert(swf.includes(Buffer.from('TRIVELA LAB'))&&swf.includes(Buffer.from('GRAMA & GO')));
console.log('Animated central fans:',fans.length);console.log('PASS: actual AS2 animation executes; moving crowd; selective home/away celebrations; string motion preference; 12-sponsor leftward seamless ribbon');
