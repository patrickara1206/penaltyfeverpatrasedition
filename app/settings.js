'use strict';
// Preferences stay separate from career saves and never execute imported content.
const PFSettings=(()=>{
 const locales={pt:'Português',en:'English',es:'Español',fr:'Français',de:'Deutsch',it:'Italiano',zh:'中文',ar:'العربية',hi:'हिन्दी',ru:'Русский'};
 const words={
 settings:['Configurações','Settings','Configuración','Paramètres','Einstellungen','Impostazioni','设置','الإعدادات','सेटिंग्स','Настройки'],
 language:['Idioma','Language','Idioma','Langue','Sprache','Lingua','语言','اللغة','भाषा','Язык'],
 access:['Acessibilidade','Accessibility','Accesibilidad','Accessibilité','Barrierefreiheit','Accessibilità','无障碍','إمكانية الوصول','सुलभता','Доступность'],
 size:['Tamanho das letras','Text size','Tamaño del texto','Taille du texte','Schriftgröße','Dimensione testo','文字大小','حجم النص','अक्षर आकार','Размер текста'],
 contrast:['Alto contraste','High contrast','Alto contraste','Contraste élevé','Hoher Kontrast','Contrasto elevato','高对比度','تباين عالٍ','उच्च कंट्रास्ट','Высокий контраст'],
 motion:['Reduzir movimentos','Reduce motion','Reducir movimiento','Réduire les animations','Bewegung reduzieren','Riduci movimento','减少动画','تقليل الحركة','गतिशीलता कम करें','Уменьшить анимацию'],
 colors:['Visão de cores','Color vision','Visión del color','Vision des couleurs','Farbsehen','Visione colori','色觉','رؤية الألوان','रंग दृष्टि','Цветовое зрение'],
 standard:['Padrão','Default','Predeterminado','Par défaut','Standard','Predefinito','默认','افتراضي','सामान्य','Обычный'],
 round:['Rodada','Round','Ronda','Tour','Runde','Turno','轮次','الجولة','दौर','Раунд'],
 attack:['Sua vez de cobrar','Your turn to shoot','Tu turno de tirar','À vous de tirer','Du schießt','Tocca a te tirare','轮到你射门','دورك للتسديد','आपकी किक','Ваш удар'],
 defend:['Adversário cobrando','Opponent’s turn','Turno del rival','Tir adverse','Gegner schießt','Tira l’avversario','对手射门','دور الخصم','विरोधी की किक','Удар соперника'],
 fullscreen:['Tela cheia','Fullscreen','Pantalla completa','Plein écran','Vollbild','Schermo intero','全屏','ملء الشاشة','पूर्ण स्क्रीन','Полный экран'],
 seasons:['Temporadas','Seasons','Temporadas','Saisons','Saisons','Stagioni','赛季','المواسم','सीज़न','Сезоны'],
 career:['Carreira','Career','Carrera','Carrière','Karriere','Carriera','生涯','المسيرة','करियर','Карьера'],
 quick:['Partida rápida','Quick match','Partido rápido','Match rapide','Schnelles Spiel','Partita rapida','快速比赛','مباراة سريعة','त्वरित मैच','Быстрый матч'],
 saves:['Meus saves','My saves','Mis partidas','Mes sauvegardes','Spielstände','Salvataggi','我的存档','المحفوظات','मेरे सेव','Сохранения'],
 rules:['Regras e identidade','Rules and identity','Reglas e identidad','Règles et identité','Regeln und Identität','Regole e identità','规则与品牌','القواعد والهوية','नियम और पहचान','Правила и стиль'],
 play:['JOGAR PARTIDA ↗','PLAY MATCH ↗','JUGAR PARTIDO ↗','JOUER ↗','SPIELEN ↗','GIOCA ↗','开始比赛 ↗','العب المباراة ↗','मैच खेलें ↗','ИГРАТЬ ↗'],
 start:['ENTRAR EM CAMPO ↗','KICK OFF ↗','AL CAMPO ↗','COUP D’ENVOI ↗','ANPFIFF ↗','SCENDI IN CAMPO ↗','开球 ↗','ابدأ ↗','किक ऑफ ↗','НАЧАТЬ ↗'],
 result:['FIM DA PARTIDA','FULL TIME','FIN DEL PARTIDO','FIN DU MATCH','SPIELENDE','FINE PARTITA','比赛结束','نهاية المباراة','मैच समाप्त','МАТЧ ОКОНЧЕН'],
 victory:['Vitória na marca da cal!','Penalty shootout victory!','¡Victoria en los penaltis!','Victoire aux tirs au but !','Sieg im Elfmeterschießen!','Vittoria ai rigori!','点球获胜！','فوز بركلات الترجيح!','पेनल्टी में जीत!','Победа по пенальти!'],
 next:['A próxima é sua.','Next time is yours.','La próxima será tuya.','La prochaine sera la vôtre.','Beim nächsten Mal!','La prossima sarà tua.','下次再战。','المرة القادمة لك.','अगली बार आपकी जीत।','В следующий раз повезёт.'],
 soundOff:['Som desligado','Sound off','Sonido apagado','Son coupé','Ton aus','Audio disattivato','声音关闭','الصوت مغلق','ध्वनि बंद','Звук выключен'],
 soundOn:['Som ligado','Sound on','Sonido activado','Son activé','Ton an','Audio attivato','声音开启','الصوت مفعل','ध्वनि चालू','Звук включён'],
 back:['Voltar à partida rápida →','Back to quick match →','Volver al partido rápido →','Retour au match rapide →','Zurück zum schnellen Spiel →','Torna alla partita rapida →','返回快速比赛 →','العودة للمباراة السريعة →','त्वरित मैच पर लौटें →','К быстрой игре →'],
 fast:['Intervalo entre cobranças','Time between kicks','Intervalo entre tiros','Pause entre les tirs','Pause zwischen Schüssen','Pausa tra i tiri','射门间隔','الفاصل بين الركلات','किक के बीच अंतराल','Интервал между ударами'],
 note:['Controles, navegação e mensagens principais disponíveis em dez idiomas. Históricos e regulamentos documentais mantêm o idioma da fonte.','Controls, navigation and main messages support ten languages. Historical records and documentary rules retain their source language.','Controles, navegación y mensajes principales en diez idiomas. Los documentos conservan su idioma original.','Commandes, navigation et messages principaux en dix langues. Les documents gardent leur langue source.','Bedienung, Navigation und Hauptmeldungen in zehn Sprachen. Dokumente behalten ihre Originalsprache.','Comandi, navigazione e messaggi principali in dieci lingue. I documenti mantengono la lingua originale.','控制、导航和主要消息支持十种语言。历史资料保留原文。','عناصر التحكم والتنقل والرسائل الرئيسية بعشر لغات. تبقى الوثائق بلغتها الأصلية.','नियंत्रण, नेविगेशन और मुख्य संदेश दस भाषाओं में। दस्तावेज़ मूल भाषा में रहते हैं।','Управление, навигация и основные сообщения на десяти языках. Документы сохраняют исходный язык.']
 };

 Object.assign(words,{
 abort:['Abandonar partida','Abandon match','Abandonar partido','Abandonner le match','Spiel aufgeben','Abbandona partita','放弃比赛','مغادرة المباراة','मैच छोड़ें','Покинуть матч'],
 exit:['Encerrar','Exit','Salir','Quitter','Beenden','Esci','退出','خروج','बाहर निकलें','Выйти'],
 attackHelp:['ATAQUE','ATTACK','ATAQUE','ATTAQUE','ANGRIFF','ATTACCO','进攻','هجوم','आक्रमण','АТАКА'],
 defendHelp:['DEFESA','DEFEND','DEFENSA','DÉFENSE','ABWEHR','DIFESA','防守','دفاع','रक्षा','ЗАЩИТА'],
 clickHelp:['· Dois cliques no tempo da corrida.','· Click twice during the run-up.','· Haz dos clics durante la carrera.','· Cliquez deux fois pendant la course.','· Zweimal beim Anlauf klicken.','· Fai due clic durante la rincorsa.','· 助跑时点击两次。','· انقر مرتين أثناء الاقتراب.','· दौड़ते समय दो बार क्लिक करें।','· Дважды нажмите во время разбега.'],
 defendClick:['· Mire no sinal vermelho e clique.','· Aim at the red marker and click.','· Apunta a la marca roja y haz clic.','· Visez le repère rouge et cliquez.','· Auf die rote Markierung zielen und klicken.','· Mira al segnale rosso e fai clic.','· 瞄准红色标记并点击。','· صوب نحو العلامة الحمراء وانقر.','· लाल निशान पर निशाना लगाकर क्लिक करें।','· Наведите на красную метку и нажмите.'],
 ready:['Pronto para cobrar','Ready to shoot','Listo para tirar','Prêt à tirer','Bereit zum Schuss','Pronto al tiro','准备射门','جاهز للتسديد','किक के लिए तैयार','Готов к удару'],
 regular:['Temporada regular','Regular season','Temporada regular','Saison régulière','Reguläre Saison','Stagione regolare','常规赛','الموسم العادي','नियमित सीज़न','Регулярный сезон'],
 opponent:['ADVERSÁRIO','OPPONENT','RIVAL','ADVERSAIRE','GEGNER','AVVERSARIO','对手','الخصم','प्रतिद्वंद्वी','СОПЕРНИК'],
 country:['PAÍS','COUNTRY','PAÍS','PAYS','LAND','PAESE','国家','الدولة','देश','СТРАНА'],
 allCountries:['Todos os países','All countries','Todos los países','Tous les pays','Alle Länder','Tutti i paesi','所有国家','كل الدول','सभी देश','Все страны'],
 allCompetitions:['Todas as competições','All competitions','Todas las competiciones','Toutes les compétitions','Alle Wettbewerbe','Tutte le competizioni','所有赛事','كل البطولات','सभी प्रतियोगिताएँ','Все турниры'],
 kickoffTitle:['ESCOLHA AS CAMISAS. DECIDA NO CAMPO.','CHOOSE YOUR CLUB. DECIDE ON THE PITCH.','ELIGE TU CLUB. DECIDE EN EL CAMPO.','CHOISISSEZ VOTRE CLUB. DÉCIDEZ SUR LE TERRAIN.','WÄHLE DEINEN VEREIN. ENTSCHEIDE AUF DEM PLATZ.','SCEGLI IL CLUB. DECIDI IN CAMPO.','选择球队，在球场决胜。','اختر ناديك واحسمها في الملعب.','अपना क्लब चुनें। मैदान में फैसला करें।','ВЫБЕРИТЕ КЛУБ. РЕШАЙТЕ НА ПОЛЕ.'],
 catalog:['CATÁLOGO','CATALOGUE','CATÁLOGO','CATALOGUE','KATALOG','CATALOGO','球队目录','الكتالوج','सूची','КАТАЛОГ'],
 level:['DIFICULDADE DA PARTIDA','MATCH DIFFICULTY','DIFICULTAD DEL PARTIDO','DIFFICULTÉ DU MATCH','SPIELSCHWIERIGKEIT','DIFFICOLTÀ PARTITA','比赛难度','صعوبة المباراة','मैच की कठिनाई','СЛОЖНОСТЬ МАТЧА'],
 club:['ESCOLHA SEU CLUBE','CHOOSE YOUR CLUB','ELIGE TU CLUB','CHOISISSEZ VOTRE CLUB','VEREIN WÄHLEN','SCEGLI IL TUO CLUB','选择球队','اختر ناديك','अपना क्लब चुनें','ВЫБЕРИТЕ КЛУБ'],
 home:['MANDANTE','HOME','LOCAL','DOMICILE','HEIM','CASA','主队','صاحب الأرض','मेज़बान','ХОЗЯЕВА'],
 away:['VISITANTE','AWAY','VISITANTE','EXTÉRIEUR','AUSWÄRTS','TRASFERTA','客队','الضيف','मेहमान','ГОСТИ']
 });
 let prefs={lang:'pt',scale:100,vision:'standard',contrast:false,motion:matchMedia('(prefers-reduced-motion: reduce)').matches,pace:75};
 try{const x=JSON.parse(localStorage.getItem('pf-settings-v105')||'{}');if(locales[x.lang])prefs.lang=x.lang;if([100,115,130,150].includes(x.scale))prefs.scale=x.scale;if(['standard','protanopia','deuteranopia','tritanopia'].includes(x.vision))prefs.vision=x.vision;for(const k of ['contrast','motion'])if(typeof x[k]==='boolean')prefs[k]=x[k];if([75,110,130].includes(x.pace))prefs.pace=x.pace}catch{}
 const index=()=>Object.keys(locales).indexOf(prefs.lang),t=k=>words[k]?.[index()]||words[k]?.[0]||k;
 const original=new WeakMap();let scheduled=false;
 function translate(){scheduled=false;const nodes=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=nodes.nextNode()){if(['SCRIPT','STYLE'].includes(n.parentElement?.tagName)||n.parentElement?.closest('.settings-panel'))continue;const value=n.nodeValue,prior=original.get(n);let src=prior&&value===prior.last?prior.source:value;const key=Object.keys(words).find(k=>words[k][0]===src.trim());if(key){const next=src.replace(src.trim(),t(key));original.set(n,{source:src,last:next});if(next!==value)n.nodeValue=next;}}}
 function apply(){document.documentElement.lang=prefs.lang==='pt'?'pt-BR':prefs.lang;document.documentElement.dir=prefs.lang==='ar'?'rtl':'ltr';document.documentElement.style.setProperty('--font-scale',String(prefs.scale/100));document.body.dataset.vision=prefs.vision;document.body.classList.toggle('high-contrast',prefs.contrast);document.body.classList.toggle('reduce-motion',prefs.motion);translate();try{localStorage.setItem('pf-settings-v105',JSON.stringify(prefs))}catch{}}
 function render(){const root=document.getElementById('content');root.innerHTML=`<section class="panel settings-panel"><span class="tag">PF · v1.0.5</span><h1>${t('settings')}</h1><label class="field" for="settingsLanguage">${t('language')}</label><select id="settingsLanguage">${Object.entries(locales).map(([k,v])=>`<option value="${k}" ${prefs.lang===k?'selected':''}>${v}</option>`).join('')}</select><h2>${t('access')}</h2><label class="field" for="settingsScale">${t('size')}</label><select id="settingsScale">${[100,115,130,150].map(x=>`<option ${x===prefs.scale?'selected':''}>${x}%</option>`).join('')}</select><label class="field" for="settingsVision">${t('colors')}</label><select id="settingsVision">${['standard','protanopia','deuteranopia','tritanopia'].map(x=>`<option value="${x}" ${x===prefs.vision?'selected':''}>${x==='standard'?t('standard'):x}</option>`).join('')}</select><label class="settings-check"><input id="settingsContrast" type="checkbox" ${prefs.contrast?'checked':''}> ${t('contrast')}</label><label class="settings-check"><input id="settingsMotion" type="checkbox" ${prefs.motion?'checked':''}> ${t('motion')}</label><label class="field" for="settingsPace">${t('fast')}</label><select id="settingsPace">${[75,110,130].map(x=>`<option value="${x}" ${x===prefs.pace?'selected':''}>${(x/40).toFixed(2)} s</option>`).join('')}</select><p class="fine">${t('note')}</p></section>`;
 for(const [id,k]of [['settingsLanguage','lang'],['settingsScale','scale'],['settingsVision','vision'],['settingsContrast','contrast'],['settingsMotion','motion'],['settingsPace','pace']])document.getElementById(id).onchange=e=>{prefs[k]=e.target.type==='checkbox'?e.target.checked:['scale','pace'].includes(k)?Number(e.target.value):e.target.value.replace('%','');if(k==='scale')prefs.scale=parseInt(e.target.value);apply();render();};}
 new MutationObserver(()=>{if(!scheduled){scheduled=true;queueMicrotask(translate)}}).observe(document.body,{childList:true,subtree:true,characterData:true});apply();
 return{t,prefs,render,apply};
})();
