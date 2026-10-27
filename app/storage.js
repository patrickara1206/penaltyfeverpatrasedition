(function(root){
'use strict';
const L=root.LZString||(typeof require==='function'?require('./lz-string.min.js'):null);
function encode(value){return'PFZ3:'+L.compressToUTF16(JSON.stringify(value))}
function decode(text){if(typeof text!=='string'||text.length>40000000)throw Error('Arquivo de salvamento excessivo');const raw=text.startsWith('PFZ3:')?L.decompressFromUTF16(text.slice(5)):text;if(!raw||raw.length>80000000)throw Error('Save corrompido ou excessivo');return JSON.parse(raw)}
root.PFStorage={encode,decode};if(typeof module!=='undefined')module.exports=root.PFStorage;
})(typeof globalThis!=='undefined'?globalThis:this);
