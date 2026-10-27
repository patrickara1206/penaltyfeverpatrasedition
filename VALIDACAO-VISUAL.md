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
