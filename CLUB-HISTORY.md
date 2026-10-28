# Histórico dos clubes

Arquivo offline: `app/club-history.js` e cópia legível `app/club-history.json`. O índice contém os 824 clubes da base atual. Não contém históricos fictícios para preencher lacunas.

## Fontes e escopo

Cada ficha documentada identifica suas fontes. A coleta usa revisões públicas da Wikipédia em português e inglês, com cache local fora do pacote. O Santos possui complemento revisado do site oficial, CBF e Prefeitura de Santos. O texto do artigo não é reproduzido: são armazenados fatos estruturados (fundação, conquistas por competição, anos e nomes de jogadores).

As contagens são de competições específicas, não um total universal de troféus. As listas podem selecionar até seis conquistas e seis nomes. Os anos mostrados podem ser uma seleção (até 25 por competição); nunca são usados para recalcular um total. Ausência de informação não significa zero títulos. As fontes podem ter critérios ou datas de atualização diferentes; a consulta em 28/10/2026 não transforma sua contagem em estatística oficial de encerramento da temporada.

`status=documented`: ao menos uma conquista ou jogador histórico encontrado. `identity-only`: identificação/fundação documentada, sem conquistas/jogadores extraídos com segurança. `unverified`: não foi encontrada correspondência segura para o clube. Os dados pendentes permanecem explicitamente vazios.

## Uniformes

As cores `kits.home` e `kits.away` são as cores que constam no infobox da fonte, quando explícitas. `patternBody` conserva o nome técnico original, quando disponível. Elas não constituem reprodução licenciada do uniforme oficial de 2026. Padrões, patrocinadores e materiais não são reconstruídos pelo coletor.

## Validação e reprodução

O gerador `tools/build_club_history.py` usa apenas a biblioteca padrão do Python. `python tools/build_club_history.py` coleta a base em português; `python tools/build_club_history.py --english` enriquece os registros sem correspondência com a base em inglês. As consultas são feitas em lotes com intervalo e cache; não há consulta à internet durante o jogo.

A correspondência exige um artigo de clube de futebol, nome/alias exato e indicação do país no texto introdutório. Canadá e País de Gales são admitidos nas ligas americana e inglesa. Equipes reservas não devem herdar títulos da equipe principal. Tabelas de vice-campeonatos, futebol feminino e categorias de base são excluídas da extração conservadora. Nem todos os formatos de artigos e predefinições são reconhecidos; por isso, a cobertura factual é parcial e os totais da seção `coverage` são o registro da execução mais recente.

## Cobertura desta versão

Em 28/10/2026: 824 fichas no índice, 610 com correspondência de fonte, 568 com fundação, 394 com conquistas e 49 com nomes históricos. 405 têm ao menos uma conquista ou nome histórico. Há 214 clubes sem correspondência segura; as demais lacunas são exibidas como dados ainda não confirmados. A pesquisa histórica completa de todos os clubes **não está concluída**.

A extração automatizada foi revisada por amostragem e endurecida para excluir homônimos, vice-campeonatos, anos extraídos de referências e linhas inconsistentes. Não equivale a uma auditoria editorial individual de todos os fatos. Os artigos e seus critérios podem mudar. Os dados preservam a fonte por ficha.

Os quadros separados de títulos podem ser enriquecidos com `python tools/enrich_history_templates.py`. Para reutilizar as respostas inglesas já armazenadas, use `python tools/build_club_history.py --english --cached`. O cache não integra o pacote distribuído. A licença dos conteúdos da Wikipédia é CC BY-SA; as fontes de origem estão atribuídas individualmente. Os fatos são estruturados, sem reprodução integral dos artigos.
