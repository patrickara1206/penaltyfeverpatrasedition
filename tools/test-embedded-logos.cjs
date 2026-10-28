'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const app=path.join(__dirname,'../app'),window={};const c=vm.createContext({window});
for(const file of ['logos.js','logos-embedded.js'])vm.runInContext(fs.readFileSync(path.join(app,file),'utf8'),c);
for(const [file,uri]of Object.entries(window.PF_EMBEDDED_LOGOS)){assert.match(uri,/^data:image\/(png|webp|svg\+xml);base64,/);assert.deepEqual(Buffer.from(uri.split(',')[1],'base64'),fs.readFileSync(path.join(app,file)),file)}
const source=fs.readFileSync(path.join(app,'app.js'),'utf8'),a=source.indexOf('function embeddedLogo('),b=source.indexOf('\nfunction updateMatchIdentity',a);c.esc=x=>String(x).replace(/[&<>"']/g,'');vm.runInContext(source.slice(a,b),c);
for(const name of Object.keys(window.PF_LOGOS.teams))assert(c.logoPath(name).startsWith('data:image/'),name);
for(const id of [...Object.keys(window.PF_LOGOS.competitions),'cont-uel','cont-uecl','cont-sud','national-euro','national-copa-america','intercontinental','club-world','cup-Brasil'])assert(c.competitionLogo({id,name:id}).includes('src="data:image/'),id);
console.log('PASS: '+Object.keys(window.PF_EMBEDDED_LOGOS).length+' embedded images match original bytes; all club paths and career competition aliases render embedded artwork');
