# Penalty Fever 2026 Edition · v1.0.6

Atualização da apresentação da partida, preservando os personagens e a física clássicos.

- Publicidade deslizando continuamente para a esquerda com 12 marcas fictícias.
- Torcida detalhada, bandeiras dos clubes e comemoração no setor do time que marcou.
- Gramado com textura de lâminas de grama e faixas de corte.
- Carregamento personalizado com os dois escudos e tela cheia preenchendo o player.
- Números originais preservados, com seleção reaplicada após cada troca de quadro do jogador.

- Física clássica original restaurada: voo, rebotes e colisões preservam o programa original, conforme solicitado.
- Alvos de defesa ocultados no início do voo; cursor restaurado.
- Goleiro do usuário em vermelho e adversário em laranja, com reaplicação da cor durante as animações.
- Detalhes adicionais de gola, costura e camisa nos personagens, preservando as animações existentes. Não é uma substituição integral dos desenhos originais.
- Placar menor, em verde escuro e dourado, com acertos verdes e erros vermelhos e símbolos distintos.
- Avisos traduzidos em maiúsculas, em faixa no canto inferior direito; rodada também em maiúsculas.
- Tela de carregamento Patras cobre a marca gráfica antiga. Créditos de autoria e licenças são preservados na documentação.
- Barragens de acesso/permanência em ida e volta na carreira: Bundesliga/2. Bundesliga, 2. Bundesliga/3. Liga e Primeira Liga/Liga Portugal 2. Equipes B não recebem vagas de acesso nesses cruzamentos.

## Regras verificadas

- [CBF: Série B 2026](https://stcbfsiteprdimgbrs.blob.core.windows.net/img-site/cdn/REC_Brasileiro_Serie_B_2026_85d55b9f72.pdf): dois acessos diretos, dois via playoffs, quatro rebaixados.
- [CBF: Série C 2026](https://stcbfsiteprdimgbrs.blob.core.windows.net/img-site/cdn/REC_Brasileiro_Serie_C_2026_d2552ddc00.pdf): dois rebaixados, preservados corretamente.
- [Bundesliga: acesso, rebaixamento e barragem](https://www.bundesliga.com/en/bundesliga/news/how-does-promotion-and-relegation-work-in-the-bundesliga-10645).
- [Liga Portugal: organização das ligas e playoffs](https://lojaoficial.ligaportugal.pt/en/liga-portugal/about-us_204.html).
- [EFL: seis participantes nos playoffs a partir de 2026/27](https://www.efl.com/news/2026/march/05/efl-statement--sky-bet-championship-play-off-format/), preservados na base.

## Validação e limites

Comparação byte a byte da física original, testes de animação do estádio, ponte do Ruffle, lançamento e resultado, catálogo, segurança, arquivos visuais e barragens da carreira. Prévia HTTP local exercitada em navegador real; não representa reprodução manual de todas as possíveis trajetórias.

Esta versão não certifica que os 91 formatos sejam integralmente oficiais. Permanecem calendários e critérios adaptados, especialmente em ligas regionais e competições com médias históricas, licenciamento ou vagas administrativas. Campanhas isoladas não disputam barragens contra outra divisão.

A cobertura de escudos continua documentada em `LOGOS-2026.md` e `app/logo-audit-current.json`: há 122 nomes atuais sem escudo confirmado e três competições sem identidade oficial confirmada. Não foram substituídos por escudos de homônimos.

Elencos continuam fictícios nesta versão. A beta 1.0.7 separada introduz elencos confirmados publicamente e fica somente no GitHub. O site de produção deve acompanhar a branch v1.0.6.
