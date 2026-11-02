'use strict';
const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const source=fs.readFileSync(__dirname+'/actionscript/physics.as','utf8');
const start=source.indexOf('ppPlane ='),end=source.indexOf('\nif(gol)',start);
const code=source.slice(start,end).replace(/\band\b/g,'&&').replace(/\bor\b/g,'||');
function crossing({x=305,y=145,px=x,py=y,previous=168,current=160,held=false}={}){
 const stub={swapDepths(){},setVolume(){},start(){}};
 const c={Math,gol:false,uRuci:held,ppPrevShadowY:previous,ppPrevBallX:px,ppPrevBallY:py,senka:{_y:current},lopta:{_x:x,_y:y,_width:8,_height:8},golLinija:168,visinaGola:80,sirinaGola:240,osaGola:305,golmance:stub,gol_senka:stub,okvirGola:stub,mrezaGornja:stub,zvukGol:stub};
 vm.runInNewContext(code,c);return c.gol;
}
assert(crossing(),'normal crossing');
assert(crossing({previous:165,current:157,px:423,x:405}),'inside after right-post deflection');
assert(crossing({previous:165,current:157,px:187,x:205}),'inside after left-post deflection');
assert(!crossing({previous:160,current:155}),'side-net entry behind plane');
assert(!crossing({previous:168,current:166}),'whole ball has not crossed');
assert(!crossing({previous:160,current:168}),'outward rebound');
assert(!crossing({held:true}),'held ball');
assert(!crossing({x:450}),'wide ball with centered shadow');
assert(!crossing({y:80}),'over bar');
assert(!crossing({px:450,x:305,previous:168,current:100}),'sweep intersection outside posts');
const builder=fs.readFileSync(__dirname+'/build_match.py','utf8');
assert(builder.includes('0x20B969')&&builder.includes('0xE74B4B'));
assert(builder.includes('0xE74636')&&builder.includes('0xF29A28'));
assert(builder.includes("put(path+'._y',346)"));
assert(builder.includes('speedhook+repaint+hide_target'));
console.log('PASS v1.0.6: 10 swept goal cases; green/red attempts; distinct keeper colors; lower-right prompt; hidden defense target');

