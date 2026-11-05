/* Portable runtime: decode only the module actually selected by Ruffle. */
(function(){
'use strict';window.PF_WASM_ASSETS=window.PF_WASM_ASSETS||{};
const realFetch=window.fetch.bind(window),pending=new Map(),responses=new Map();
function load(name){if(!pending.has(name))pending.set(name,(async()=>{for(const src of window.PF_WASM_MODULES[name])await new Promise((resolve,reject)=>{const s=document.createElement('script');s.src=src;s.onload=resolve;s.onerror=()=>reject(Error('Não foi possível preparar o motor do jogo. Reabra o pacote completo.'));document.head.append(s)})})());return pending.get(name)}
window.fetch=async function(input,options){const u=typeof input==='string'?input:input instanceof URL?input.href:input.url,name=u.split('/').pop().split('?')[0];if(Object.hasOwn(window.PF_WASM_MODULES||{},name)){await load(name);if(!responses.has(name)){const bytes=Uint8Array.from(atob(window.PF_WASM_ASSETS[name]),c=>c.charCodeAt(0));delete window.PF_WASM_ASSETS[name];responses.set(name,new Response(bytes,{status:200,headers:{'Content-Type':'application/wasm'}}))}return responses.get(name).clone()}return realFetch(input,options)};
})();
