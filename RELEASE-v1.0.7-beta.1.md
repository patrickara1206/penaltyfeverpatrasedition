# v1.0.7-beta.1 · teste de elencos confirmados

Esta beta contém todas as alterações da v1.0.6 e acrescenta a primeira base de elencos públicos verificados. Somente GitHub: não publicar no site de produção.

## Cobertura inicial

Consulta em 2 de novembro de 2026:

- [Palmeiras](https://www.palmeiras.com.br/elenco/): 25 jogadores.
- [Santos](https://www.santosfc.com.br/masculino/): 34 jogadores.
- [Botafogo](https://www.botafogo.com.br/elenco/futebol): 32 jogadores.

São os 91 nomes presentes nas páginas públicas dos clubes, não uma declaração de inscrição em todas as competições. Não se incluem emprestados listados separadamente pelo Palmeiras. Numeração ausente na página consultada permanece vazia. Não foram importadas fotografias, datas de nascimento ou outros dados pessoais.

Os demais clubes continuam com elencos fictícios explicitamente identificados. A cobertura não é completa; os nomes não confirmados não são apresentados como oficiais. Competições históricas ainda não possuem elencos verificados por edição.

## Funcionamento

Jogadores confirmados aparecem nas cobranças e na carreira; goleiros adicionais não entram na rotação de cobradores. A seleção de equipes e a tela da temporada permitem abrir a lista e consultar a fonte. A rotação usa todos os jogadores de linha disponíveis, sem alterar o equilíbrio da dificuldade.

`app/rosters-verified.json` registra fonte, consulta, escopo, nomes, posições, números disponíveis e SHA256 do HTML consultado. O arquivo JS incorpora os mesmos dados para execução offline.

## Separação de produção

Produção permanece na branch v1.0.6. Previews automáticos de outras branches foram desativados no Pages. Commits da beta usam `[CF-Pages-Skip]`. O builder da beta também recusa execução dentro do Cloudflare Pages/Workers CI, evitando publicação acidental.

Testes verificam a fonte por clube, consistência entre JSON e JS, nomes válidos, exclusão de goleiros das cobranças, ausência de números inventados e identificação dos elencos fictícios. Permanecem os limites de formatos e escudos documentados na v1.0.6.
