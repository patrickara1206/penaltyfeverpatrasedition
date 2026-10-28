# v1.0.4 · Prévia de expansão

Esta release reúne as mudanças funcionais solicitadas e uma expansão jogável do catálogo. **A base ainda não está integralmente confirmada, e vários formatos oficiais continuam simplificados.** Por isso, a versão é distribuída como prévia; a v1.0.3 permanece a estável.

## O que mudou

- Randomizar e Restaurar os grupos, antes da primeira partida, mantendo participantes e tamanhos dos grupos.
- Tabelas alinhadas e cores de classificação, playoffs, torneios secundários e rebaixamento; no Brasil: quatro azuis, um laranja, seis verdes e quatro vermelhos.
- Filtros por país na tela inicial; país, torneio e divisão no Mundo do futebol.
- Tela cheia durante os pênaltis, com retorno ao modo normal.
- Regras iniciam recolhidas.
- Histórico de cinco partidas rápidas, dez campanhas e cinco carreiras, com remoção FIFO do registro mais antigo ao ultrapassar o limite. Botão Deletar com confirmação nas listagens.
- Calendário interativo de clube/seleção, filtros de mês e competição, jogos conhecidos intercalados e fases condicionais identificadas.
- Simulação balanceada pelos quatro níveis de dificuldade; o acesso à simulação individual ou completa não permite pular uma final controlada pelo jogador.
- Cargo de seleção expira quatro anos depois do último título intercontinental.
- Sala de Troféus exclusiva da carreira, com ilustração própria, clube e ano.
- Janela de dez anos no histórico e anuário, com aviso antes de iniciar o ano que exclui registros; os troféus são preservados.

## Catálogo e cobertura

91 competições, incluindo 22 Copas históricas (1930–2022), a Copa de 2026 e Eurocopa/Copa América de 2024. Não houve Copa em 1942 ou 1946. Participantes históricos e a estrutura principal das edições foram incluídos: mata-mata em 1934/1938, quadrangular final em 1950, segunda fase de grupos em 1974/1978/1982, melhores terceiros em 1986/1990/1994 e oito grupos nas edições de 1998 a 2022. As vitórias anteriores a 1994 valem dois pontos.

Foram adicionadas três categorias de Portugal, Arábia Saudita, Colômbia, Uruguai, Equador, Japão, Rússia, África do Sul e Egito. A Primeira C colombiana é amadora e não tem acesso automático à segunda divisão profissional. O Japão usa a temporada regular 2026/27, não o torneio especial de transição.

**Recortes parciais, visíveis também no jogo:**

- ABC Motsepe: 48 clubes de streams de Mpumalanga e Western Cape; faltam as demais províncias.
- Egito Second Division B: 38 clubes identificados; composição integral dos grupos pendente de confirmação.
- Equador Segunda Categoría: 47 identidades únicas na fase nacional; uma entrada ambígua na fonte impede confirmar todos os 48 clubes e os grupos completos.

Sul-Americana, Liga Europa, Conferência, Supercopa da UEFA e qualificatórios europeus foram adicionados. **Os playoffs da Sul-Americana não estão interligados aos terceiros da Libertadores. As rotas de qualificação europeias foram reduzidas a chaves próprias, sem todas as entradas escalonadas e transferências entre torneios.** Diversas ligas novas usam uma temporada de ida e volta ou grupos adaptados, em vez de todas as fases de seus regulamentos nacionais. Os calendários são gerados pelo jogo, não oficiais. As cores das vagas são projeções das regras adaptadas da carreira.

Os 57 emblemas novos de competições e os monogramas de equipes adicionais são artes próprias PF, não logos oficiais licenciados. Os escudos já presentes foram preservados. Fichas históricas novas sem pesquisa específica ficam identificadas como não documentadas; não recebem títulos ou ídolos inventados. Uniformes são estilizados e cobradores fictícios.

## Compatibilidade e testes

Os saves anteriores mantêm o universo de divisões de sua criação. Crie uma carreira nova para incluir todas as ligas adicionais. Antes de importar ou criar vários registros, exporte uma cópia: os novos limites FIFO são aplicados ao salvar. Fechar uma partida em andamento mantém a regra de abandono.

Testes de motor: 91 competições concluídas, sorteio/restauração, bloqueio de finais, quatro dificuldades, 455 temporadas de competição e 77 anos de carreira, em 18 países, retenção de histórico e expiração de seleção. Regressões de segurança, ponte do Ruffle, artes e uniformes também verificadas. Prévia HTTP em navegador: sorteio/restauração, confirmação/cancelamento de exclusão, filtros, calendário intercalado, tabela com zonas, sala de troféus vazia, final obrigatória e entrada/saída de tela cheia. A execução por duplo clique em todos os sistemas e navegadores não foi validada.

## Fontes

Cada competição tem fonte e ressalvas em CATALOGO-v1.0.4.json e em Regras e identidade. Referências de estrutura: FIFA (história das Copas), UEFA (formatos europeus), CONMEBOL (manual Sudamericana 2026), J.League, SAFF, AUF, DIFUTBOL e FEF. As listas foram cotejadas com páginas de temporada; as lacunas acima permanecem abertas.
