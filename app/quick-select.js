'use strict';
/* Carousel model is shared with its tests; no third-party UI dependency. */
(function(root){
'use strict';
const normalize=s=>String(s).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase('pt-BR');
const country=c=>c.country||(c.id==='argc'?'Argentina':c.region==='Seleções'?'Seleções':'Internacionais');
function leagues(data,selected){return data.competitions.filter(c=>!c.historical&&(selected==='all'||country(c)===selected));}
function list(data,catalog,selectedCountry='all',league='all',query=''){
 const pool=catalog==='archive'?data.archive:leagues(data,selectedCountry).filter(c=>league==='all'||c.id===league).flatMap(c=>c.teams);
 const q=normalize(query.trim());return [...new Set(pool)].filter(n=>normalize(n).includes(q)).sort((a,b)=>a.localeCompare(b,'pt-BR'));
}
function step(index,delta,length){return length?((index+delta)%length+length)%length:-1;}
function slots(index,length){const seen=new Set(),result=[];for(const offset of [0,-1,1,-2,2]){const at=step(index,offset,length);if(at<0||seen.has(at))continue;seen.add(at);result.push({offset,index:at});}return result.sort((a,b)=>a.offset-b.offset);}
const api={normalize,country,leagues,list,step,slots};root.PFQuickModel=api;if(typeof module!=='undefined')module.exports=api;
})(typeof globalThis!=='undefined'?globalThis:this);
let quickSelection={catalog:'current',level:1,home:{country:'Brasil',league:'br0',query:'',name:'Flamengo'},away:{country:'Brasil',league:'br0',query:'',name:'Palmeiras'}};
function quickSideLabel(side){return side==='home'?'seu time':'adversário';}
function quickCountryOptions(selected){const countries=[...new Set(data.competitions.map(PFQuickModel.country))].sort((a,b)=>a==='Brasil'?-1:b==='Brasil'?1:a.localeCompare(b,'pt-BR'));return `<option value="all">Todos os países</option>`+options(countries,selected);}
function quickLeagueOptions(country,selected){return '<option value="all">Todas as competições</option>'+PFQuickModel.leagues(data,country).map(c=>`<option value="${esc(c.id)}" ${c.id===selected?'selected':''}>${esc(c.name)}</option>`).join('');}
function quickSideHtml(side){const s=quickSelection[side],label=quickSideLabel(side),archive=quickSelection.catalog==='archive';return `<section class="club-picker" aria-label="Escolher ${label}"><div class="picker-heading"><span class="picker-side">${side==='home'?'01 · VOCÊ CONTROLA':'02 · ADVERSÁRIO'}</span><span class="picker-ready">ESCOLHA SEU CLUBE</span></div><div class="picker-filters ${archive?'hide':''}"><div><label class="field" for="${side}Country">PAÍS · ${label.toUpperCase()}</label><select id="${side}Country">${quickCountryOptions(s.country)}</select></div><div><label class="field" for="${side}League">COMPETIÇÃO · ${label.toUpperCase()}</label><select id="${side}League">${quickLeagueOptions(s.country,s.league)}</select></div></div><div class="club-orbit"><img class="selection-globe" src="selection-globe.svg" alt=""><div class="orbit-lines" aria-hidden="true"></div><button class="wheel-arrow previous" data-step="-1" data-side="${side}" aria-label="Clube anterior — ${label}">‹</button><div id="${side}Wheel" class="club-wheel" tabindex="0" role="group" aria-label="Clubes — ${label}. Use as setas para trocar."></div><button class="wheel-arrow next" data-step="1" data-side="${side}" aria-label="Próximo clube — ${label}">›</button></div><div id="${side}Identity" class="picker-identity" aria-live="polite" aria-atomic="true"></div><div id="${side}Ticks" class="wheel-ticks" aria-hidden="true"></div><div class="picker-search"><label class="field" for="${side}Search">BUSCAR CLUBE · ${label.toUpperCase()}</label><input id="${side}Search" type="search" maxlength="80" autocomplete="off" placeholder="Digite o nome do clube…" value="${esc(s.query)}"></div><p class="picker-hint">← → para trocar · Home/End para primeiro/último</p></section>`;}
function renderQuick(){
 $('content').innerHTML=`<section class="quick-arena"><div class="arena-heading"><div><span class="tag">ESCOLHA AS CAMISAS. DECIDA NO CAMPO.</span><h1>Partida rápida</h1></div></div><div class="arena-options"><div><label class="field" for="quickCatalog">CATÁLOGO</label><select id="quickCatalog"><option value="current" ${quickSelection.catalog==='current'?'selected':''}>Equipes das temporadas atuais</option><option value="archive" ${quickSelection.catalog==='archive'?'selected':''}>Arquivo clássico · dados históricos</option></select></div><div><label class="field" for="quickDifficulty">DIFICULDADE DA PARTIDA</label><select id="quickDifficulty">${F.levels.map((n,i)=>`<option value="${i}" ${i===quickSelection.level?'selected':''}>${n}</option>`).join('')}</select></div></div><div class="club-pickers">${quickSideHtml('home')}${quickSideHtml('away')}</div><div class="quick-kickoff"><p id="quickMatchSummary" class="quick-match-summary"></p><button class="primary" id="quickStart">ENTRAR EM CAMPO ↗</button><p class="fine">Esta partida não altera suas temporadas. Empate leva à morte súbita.</p><p class="fine">No arquivo clássico, nomes e dados são históricos; não são participantes atualizados de 2026.</p></div></section>`;
 for(const side of ['home','away']){
  $(side+'Country').onchange=()=>{quickSelection[side].country=$(side+'Country').value;quickSelection[side].league='all';quickSelection[side].query='';$(side+'Search').value='';$(side+'League').innerHTML=quickLeagueOptions(quickSelection[side].country,'all');paintQuickSide(side);};
  $(side+'League').onchange=()=>{quickSelection[side].league=$(side+'League').value;quickSelection[side].query='';$(side+'Search').value='';paintQuickSide(side);};
  $(side+'Search').oninput=()=>{quickSelection[side].query=$(side+'Search').value;paintQuickSide(side);};
  $(side+'Wheel').onkeydown=e=>{const delta={ArrowLeft:-1,ArrowRight:1};if(Object.hasOwn(delta,e.key)){e.preventDefault();moveQuickSide(side,delta[e.key]);}else if(e.key==='Home'||e.key==='End'){e.preventDefault();const list=quickList(side);quickSelection[side].name=list[e.key==='Home'?0:list.length-1]||'';paintQuickSide(side);}};
  paintQuickSide(side);
 }
 document.querySelectorAll('[data-step]').forEach(b=>b.onclick=()=>moveQuickSide(b.dataset.side,Number(b.dataset.step)));
 $('quickCatalog').onchange=()=>{quickSelection.catalog=$('quickCatalog').value;for(const side of ['home','away']){quickSelection[side]={country:'all',league:'all',query:'',name:side==='home'?'Flamengo':'Palmeiras'};}renderQuick();};
 $('quickDifficulty').onchange=()=>{quickSelection.level=Number($('quickDifficulty').value);};
 $('quickStart').onclick=()=>{const h=quickSelection.home.name,a=quickSelection.away.name;if(!h||!a)return;if(h===a){toast('Escolha duas equipes diferentes.');return;}startMatch({home:h,away:a,user:h,kind:'quick',draw:false,manualLevel:quickSelection.level});};
}
function quickList(side){const s=quickSelection[side];return PFQuickModel.list(data,quickSelection.catalog,s.country,s.league,s.query);}
function moveQuickSide(side,delta){const list=quickList(side),s=quickSelection[side];s.name=list[PFQuickModel.step(list.indexOf(s.name),delta,list.length)]||'';paintQuickSide(side,delta);}
function paintQuickSide(side,direction=0){
 const s=quickSelection[side],list=quickList(side);if(!list.includes(s.name))s.name=list[0]||'';const index=list.indexOf(s.name),wheel=$(side+'Wheel');
 wheel.innerHTML=PFQuickModel.slots(index,list.length).map(slot=>{const n=list[slot.index];return slot.offset===0?`<div class="wheel-slot selected" data-offset="0"><div class="orbit-ring"></div><div class="orbit-crest">${teamLogo(n)}</div></div>`:`<button class="wheel-slot neighbour" data-offset="${slot.offset}" data-pick="${slot.index}" aria-label="Selecionar ${esc(n)}"><span class="neighbour-crest">${teamLogo(n)}</span></button>`;}).join('');
 wheel.classList.remove('move-left','move-right');if(direction)wheel.classList.add(direction<0?'move-left':'move-right');
 wheel.querySelectorAll('[data-pick]').forEach(b=>b.onclick=()=>{s.name=list[Number(b.dataset.pick)];paintQuickSide(side);wheel.focus({preventScroll:true});});
 const comp=quickSelection.catalog==='current'?data.competitions.find(c=>(s.league==='all'||c.id===s.league)&&c.teams.includes(s.name)):null,history=window.PP_CLUB_HISTORY?.teams?.[s.name];
 $(side+'Identity').innerHTML=s.name?`<h2>${esc(s.name)}</h2><p class="picker-league">${esc(comp?.name||'Arquivo clássico')} ${comp?'· '+esc(comp.season):''}</p><div class="picker-facts"><span><small>FUNDAÇÃO</small><b>${esc(history?.founded||'—')}</b></span><span><small>NO FILTRO</small><b>${list.length} ${list.length===1?'EQUIPE':'EQUIPES'}</b></span><span><small>SELEÇÃO</small><b>${String(index+1).padStart(2,'0')} / ${list.length}</b></span></div>`:'<h2>Nenhum clube encontrado</h2><p class="picker-league">Tente outro nome ou limpe a busca.</p>';
 $(side+'Ticks').innerHTML=Array.from({length:Math.min(list.length,20)},(_,i)=>`<i class="${i===(index%20)?'active':''}"></i>`).join('');
 document.querySelectorAll(`[data-step][data-side="${side}"]`).forEach(b=>b.disabled=list.length<2);
 if($('quickMatchSummary'))$('quickMatchSummary').textContent=(quickSelection.home.name||'Escolha seu time')+' × '+(quickSelection.away.name||'Escolha o adversário');
 if($('quickStart'))$('quickStart').disabled=!quickSelection.home.name||!quickSelection.away.name;
}
