/* Local input boundary. No secrets, server session or remote write access. */
(function(root){
'use strict';
const MAX_JSON=80000000,MAX_FILE=80000000,MAX_NODES=2000000,MAX_DEPTH=64;
const denied=new Set(['__proto__','prototype','constructor']);
function inspect(value){
 const stack=[[value,0]],seen=new Set();let nodes=0;
 while(stack.length){const [v,depth]=stack.pop();if(++nodes>MAX_NODES||depth>MAX_DEPTH)throw Error('Save excede o limite de estrutura');
  if(typeof v==='number'&&!Number.isFinite(v))throw Error('Número inválido no save');
  if(typeof v==='string'&&v.length>2000000)throw Error('Texto excessivo no save');
  if(v&&typeof v==='object'){
   if(seen.has(v))throw Error('Estrutura circular no save');seen.add(v);
   const proto=Object.getPrototypeOf(v);if(!Array.isArray(v)&&proto!==Object.prototype&&proto!==null)throw Error('Objeto inválido no save');
   for(const key of Object.keys(v)){if(denied.has(key))throw Error('Chave insegura no save');if(key.length>256)throw Error('Chave excessiva no save');stack.push([v[key],depth+1]);}
  }else if(!['string','number','boolean','undefined'].includes(typeof v)&&v!==null)throw Error('Valor inválido no save');
 }
 return value;
}
function parseJSON(text){if(typeof text!=='string'||text.length>MAX_JSON)throw Error('Arquivo de salvamento excessivo');return inspect(JSON.parse(text));}
function safeURL(value){try{const url=new URL(value);return url.protocol==='https:'?url.href:'#';}catch{return '#';}}
const api={inspect,parseJSON,safeURL,MAX_JSON,MAX_FILE};root.PFSecurity=api;if(typeof module!=='undefined')module.exports=api;
})(typeof globalThis!=='undefined'?globalThis:this);
