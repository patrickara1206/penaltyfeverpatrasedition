# Validação da interface — 27/10/2026

Prévia HTTP local em navegador Chromium, sem alterar suas proteções. Nenhum erro ou aviso de console ao fim do teste.

- Menu com PF e 34 competições; Carreira ao lado de Temporadas.
- Partida rápida real: Flamengo × Internacional, resultado 1 × 3.
- Uniforme do Flamengo manteve as cores na corrida. Uniforme do Deportivo azul/branco e calção azul conferido na versão final.
- Botão de som alterou o estado durante o confronto.
- Confirmação de abandono: Continuar jogando retomou a partida; confirmação registrou 0 × 5 e uma derrota na carreira.
- Recarregar durante outro jogo registrou 0 × 2 ao reabrir. A carreira passou a ter duas derrotas.
- Consulta Mundo do futebol durante o jogo: tabela do Championship acessível, confronto pausado e retomado.
- Exportação real de um JSON e importação pelo seletor de arquivos: validação concluída e progresso preservado.
- Partida real da Carreira: Flamengo × Cruzeiro, resultado 2 × 4. Depois, 3 partidas, 3 derrotas, 2 gols; tabela do Flamengo com 0 pontos e saldo −9, incluindo os abandonos anteriores.
- Simulação do restante de 2026: resumo com campeões de ligas, copas, continentais, Intercontinental e Copa do Mundo, além de acessos/rebaixamentos.
- Proposta do Almería recusada; proposta do Deportivo La Coruña aceita para 2027. Histórico preservou Flamengo, rebaixamento, recusa e transferência.
- Save retomado após recarregar; dados de teste pertencem apenas à prévia do navegador, não são incluídos como progresso inicial do pacote.

Prévias em `previas/`. O relatório automatizado independente está em `VALIDACAO.json`; o script reproduzível é `tools/test-game.cjs`.

## Limite de validação

A abertura direta `file:` foi bloqueada pela política do navegador de testes. O carregador offline e seus módulos WebAssembly passaram em verificação sem rede, mas o duplo clique no pacote extraído não foi testado em cada sistema operacional. Teste em HTTP local não comprova comportamento de todos os navegadores com arquivos locais. Windows/macOS/Linux precisam de navegador moderno com JavaScript/WebAssembly; não há garantia para computadores antigos ou restritos.

## Atualização visual e correção da corrida

Placar e gramado modernizados: painel opaco com gols destacados, cinco indicadores por equipe com maior espaçamento, caixa de rodada de 100 × 30 com texto centralizado. Gramado vetorial com faixas em perspectiva e textura leve. Conferido no navegador em Santos × Atlético-MG: primeira cobrança perdida pelo Santos, conversão do Atlético-MG, placar 0 × 1 e RODADA 2, sem avisos ou erros no console. Prévia: `previas/placar-gramado.png`. Alteração restrita ao desenho; trajetória, controles e resolução das cobranças preservados.

Arquibancada e placas fictícias conferidas no navegador, atrás da rede. Logos dos clubes conferidas na seleção e no cabeçalho. Marca RODADA e cinco indicadores por equipe adicionados ao placar. Leitura real de RGB percorreu os 20 quadros de ambos os times, sem divergências (VALIDACAO-CORES.json). Todos os arquivos dos 888 nomes e das 34 competições passaram na validação de formato e integridade (VALIDACAO-VISUAL-ASSETS.json).

Placar de pênaltis validado em uma partida real encerrada em 0 × 2: quatro perdas do mandante e duas conversões/uma perda do visitante, encerramento antecipado normal. Os círculos e os gols acompanharam os eventos reais; RODADA atualizou junto com as cobranças. Dados em VALIDACAO-PENALTIS.json. O escudo da seleção de equipe também foi conferido em tela menor.

## Revisão v1.0.1

Identidade refeita com escudo PF, verde de campo e dourado; marca do cabeçalho retorna ao início. Cartões de competições revelam a logo ampliada no hover e no foco por teclado, com halo de contraste e respeito à redução de movimento. Regras reorganizadas por assunto. Personalização livre substituída por Casa/Fora, com seleção persistida e representações estilizadas.

Histórico consultado offline no painel do clube, com títulos de escopo definido, anos e fontes. Pesquisa parcial: ver CLUB-HISTORY.md. Teste de integração em VALIDACAO-EDICAO.json verifica 1.776 escolhas de uniforme para 888 nomes e a estrutura/fonte das 824 fichas. Esse teste não comprova sozinho a exatidão editorial de cada fato.

Partida real Santos × Botafogo na v1.0.1: Santos com o preset Fora listrado, duas conversões na primeira rodada, placar 1 × 1 e RODADA 2. Tela inicial, fonte histórica do Santos, modal Casa/Fora, retorno pela marca e guia de regras conferidos no navegador. Prévia preservada para revisão do usuário.

## Revisão v1.0.2

Halo e animação dos escudos na seleção de clube e na Partida rápida. Interface e Ruffle iniciados com a CSP restrita em prévia HTTP local, sem erros de console. Guardas de entrada e descompressão verificados em VALIDACAO-SEGURANCA.json. Limites e ameaças cobertas em SECURITY.md.

## Revisão v1.0.3

Carrosséis conferidos com mouse, teclado e busca sem acentos. Busca vazia desabilita a entrada. Filtros de Inglaterra/Premier League e Itália/Serie A levaram a Manchester United × Inter de Milão, iniciados corretamente no Ruffle, sem avisos no console. Layouts de 714, 840 e 1280 px conferidos; sem rolagem horizontal nas larguras medidas. Redução de movimento respeitada pelo CSS. O modelo testa todas as 34 competições e listas de zero, uma, duas e muitas equipes.

## Correção de partidas na v1.0.3

Restaurada a função de entrada da temporada (`launchSeason`). A ponte ExternalInterface dos dois módulos locais do Ruffle passou a despachar exclusivamente patrasReady, patrasTurn, patrasShot, patrasProgress e patrasResult, sem compilar strings JavaScript. A CSP continua sem unsafe-eval. Os módulos receberam nomes derivados do conteúdo e as entradas alteradas usam revisão de cache 103.1.

Regressão: `node tools/test-match-bridge.cjs` verifica entrada da temporada, placar final, histórico, retorno à seleção e callback duplicado; executa as duas pontes com geração dinâmica de código desabilitada e recusa nomes/código arbitrários.

Validação em navegador HTTP local: partida rápida Flamengo × Palmeiras completada em 0 × 3; resultado visível, botão de retorno funcionando. Temporada Série A iniciada como Santos, botão JOGAR PARTIDA abriu Santos × Botafogo com motor, identidade e callbacks ativos. Evidências: previas/resultado-corrigido-v103.png e previas/temporada-corrigida-v103.png.
