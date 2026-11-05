/* Source-backed rosters. No penalty order is inferred for uncovered clubs. */
(function(root){
'use strict';
function record(club,comp){if(comp?.historical&&comp.id.startsWith('world-'))return root.ME_WORLD_CUP?.[comp.season+'::'+club]||null;return root.ME_NATIONAL_PLAYERS?.[String(comp?.season??2026)+'::'+club]||(!comp?.historical?root.ME_NATIONAL_PLAYERS?.['2026::'+club]:null)||root.ME_CURRENT_PLAYERS?.[club]||null}
function lineup(club,comp){const r=record(club,comp);if(!r)return null;const keep=r.players.find(p=>p.role==='Goleiro')||{name:'Goleiro',role:'Goleiro',number:1};return[keep,...r.players.filter(p=>p!==keep)]}
function kicker(club,comp,turn){const r=record(club,comp),players=r?.players.filter(p=>p.role!=='Goleiro'||r.penaltyOrderIds?.includes(p.id));if(!players?.length)return{name:'Cobrador '+(turn+1),role:'Cobrador',number:0,verified:false,orderVerified:false};return{...players[turn%players.length],verified:true,orderVerified:!!r.orderVerified&&(!r.penaltyOrderIds||r.penaltyOrderIds.includes(players[turn%players.length].id)),orderDate:r.orderDate,source:r.source,year:r.year||r.season}}
root.MEPlayers={record,lineup,kicker};
})(window);
