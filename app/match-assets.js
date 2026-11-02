/* Embed only the selected two crests into the match, including offline play. */
(function(root){
'use strict';
const concat=parts=>{const out=new Uint8Array(parts.reduce((n,p)=>n+p.length,0));let at=0;for(const p of parts){out.set(p,at);at+=p.length}return out};
function u16(v){return Uint8Array.of(v&255,v>>8&255)}
function u32(v){return Uint8Array.of(v&255,v>>8&255,v>>16&255,v>>>24)}
function tag(code,payload){return concat([u16(code<<6|63),u32(payload.length),payload])}
async function zip(bytes,inverse=false){const stream=new Blob([bytes]).stream().pipeThrough(inverse?new DecompressionStream('deflate'):new CompressionStream('deflate'));return new Uint8Array(await new Response(stream).arrayBuffer())}
async function crest(src,id,name){if(!src)return null;const image=new Image();image.src=src;await image.decode();if(!image.naturalWidth) return null;const canvas=document.createElement('canvas');canvas.width=canvas.height=64;const ctx=canvas.getContext('2d'),s=60/Math.max(image.naturalWidth,image.naturalHeight),w=image.naturalWidth*s,h=image.naturalHeight*s;ctx.drawImage(image,(64-w)/2,(64-h)/2,w,h);const rgba=ctx.getImageData(0,0,64,64).data,argb=new Uint8Array(rgba.length);for(let i=0;i<rgba.length;i+=4){const a=rgba[i+3];argb[i]=a;argb[i+1]=Math.round(rgba[i]*a/255);argb[i+2]=Math.round(rgba[i+1]*a/255);argb[i+3]=Math.round(rgba[i+2]*a/255)}return{id,name,tag:tag(36,concat([u16(id),Uint8Array.of(5),u16(64),u16(64),await zip(argb)]))}}
async function withFlags(bytes,sources){if(typeof CompressionStream==='undefined'||typeof DecompressionStream==='undefined')return bytes;try{const assets=(await Promise.all(sources.map((src,i)=>crest(src,30000+i,'pf_'+(i?'away':'home')+'_crest').catch(()=>null)))).filter(Boolean);if(!assets.length)return bytes;const body=bytes[0]===67?await zip(bytes.slice(8),true):bytes.slice(8),rect=(5+4*(body[0]>>3)+7)>>3,start=rect+4;const exports=tag(56,concat([u16(assets.length),...assets.map(a=>concat([u16(a.id),new TextEncoder().encode(a.name+'\0')]))]));const full=concat([body.slice(0,start),...assets.map(a=>a.tag),exports,body.slice(start)]);return concat([Uint8Array.of(67,87,83,bytes[3]),u32(full.length+8),await zip(full)])}catch{return bytes}}
root.PFMatchAssets={withFlags};
})(window);
