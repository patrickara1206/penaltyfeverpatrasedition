'use strict';
$('fullscreen').onclick=toggleMatchFullscreen;document.addEventListener('fullscreenchange',()=>{$('fullscreen').textContent=document.fullscreenElement?'Sair da tela cheia':'Tela cheia'});$('deleteSaveCancel').onclick=()=>$('deleteSaveDialog').close();$('historyWarningCancel').onclick=()=>$('historyWarning').close();
