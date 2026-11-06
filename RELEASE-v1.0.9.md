# Na Marca · v1.0.9

## Correção de cobranças e defesas

Restaurados os programas originais completos de preparação, mouse, corrida, mira, decisão do goleiro, trajetória, colisão e escala da bola. Removidas as interferências de velocidade, mira e temporização adicionadas por esta edição. O ajuste de intervalo que cortava a animação foi retirado das configurações; as preferências antigas continuam compatíveis. Visual, uniformes, gramado, torcida, placar, anúncios, elencos, agenda e carregamento sob demanda foram mantidos.

O teste compara byte a byte as seis fases nativas e rejeita intervenções extras nos controles. A tag original e os pacotes anteriores são preservados; o ZIP principal da release recebe a correção.

Nova identidade em verde, azul, amarelo e branco, mantendo a partida aprovada da v1.0.6: física original, gramado, torcida, números das camisas e placar.

- Dificuldade: usa a progressão nativa do clássico, sem forçar a mira do goleiro nem mudar a velocidade da bola.
- Menus sem pré-carregar os dois motores WebAssembly e o catálogo inteiro de imagens incorporadas. Preparação do mesmo confronto reaproveitada; superfícies estáticas e textos de placar evitam trabalho redundante.
- Elencos históricos para as 489 participações em Copas de 1930 a 2022; 88 elencos das edições recentes incluídas. Os dados se referem ao elenco da edição, sem afirmar que todos entraram em campo.
- 438 elencos de clubes documentados, com 14.909 nomes. Em 209 clubes, a última disputa localizada nos calendários consultados fornece a ordem dos cobradores que continuam no elenco. Os demais jogadores não recebem uma ordem presumida.
- 436 escudos atualizados a partir das páginas de equipes da ESPN; catálogo local preservado para as demais equipes, com imagens incorporadas no pacote portátil.
- Aba Partidas do dia, consultando 17 competições, com horário de Brasília, cancelamento de consultas antigas e agenda datada para uso offline.
- Sete fotografias documentadas de troféus, com autoria e licença na sala de conquistas; títulos anteriores permanecem compatíveis.
- Novos anúncios fictícios: Ardidas, Mike, Petshoes, Cola Coca e Guaraná Aleluia.

## Cobertura e limitações

Esta entrega não certifica que todos os clubes, escudos, troféus ou regulamentos sejam 100% oficiais e atuais. Ainda há clubes sem elenco confirmado, 122 escudos de contingência e três imagens de competições sem confirmação. As competições com regras adaptadas e os recortes parciais continuam indicados na interface. A carreira contém copas e temporadas futuras adaptadas ao jogo. Sete modelos de troféus possuem fotografia; as demais conquistas mantêm ilustração identificada. Consulte DADOS-v1.0.9.md e os relatórios de cobertura.

Os ajustes de carregamento não garantem fluidez em todo computador. A tradução cobre os controles e termos cadastrados, sem prometer tradução integral de todas as telas. A base v1.0.6 e a beta v1.0.7 permanecem separadas.

## Executar

Extraia o ZIP inteiro e abra JOGAR.html em navegador moderno com JavaScript/WebAssembly. Não requer instalação nem administrador. Exporte seus saves antes de trocar de navegador ou computador; os identificadores de armazenamento existentes foram preservados.
