# Segurança — PF v1.0.2

O jogo é estático, sem API de escrita, login, banco de dados de usuários, pagamentos ou ranking compartilhado. Os saves ficam no navegador e podem ser exportados. Não há credenciais de produção no código.

## Controles implementados

- CSP com scripts locais, sem JavaScript inline nem `unsafe-eval`; `wasm-unsafe-eval` permite o WebAssembly necessário ao Ruffle.
- Conexões de rede do jogo, formulários, frames, plugins e alteração da URL-base bloqueados pela CSP. Imagens e scripts são locais. Estilos inline continuam necessários para representar uniformes e cores.
- Importação e leitura local rejeitam chaves `__proto__`, `constructor` e `prototype`, objetos inesperados, profundidade acima de 64 níveis, mais de 2 milhões de nós, strings excessivas e números não finitos.
- Limites de arquivo/JSON de 80 milhões de caracteres/bytes e de armazenamento comprimido de 40 milhões de caracteres. A expansão LZ é limitada durante a descompressão; dicionários também têm limite.
- Validações específicas de clubes, competições, partidas e carreiras continuam ativas. Nomes e textos de saves são escapados antes de entrar no HTML. Eventos que interpolavam IDs em JavaScript inline foram substituídos por atributos de dados e handlers locais.
- Links de fontes são limitados a HTTPS. O site publicado usa HTTPS do GitHub Pages.

## Limites

Esses controles reduzem riscos; não garantem invulnerabilidade e não constituem uma auditoria profissional completa. O visitante controla seu navegador e pode alterar um save local; não existe anti-cheat com autoridade de servidor. Não guarde segredos nos saves.

A CSP é entregue por meta tag no GitHub Pages. Algumas diretivas, como `frame-ancestors`, exigem cabeçalho HTTP e não são aplicadas por essa configuração. Não alegamos proteção de cabeçalhos que o provedor não fornece. Uma futura API/login/ranking exigirá validação e autorização no servidor, limites de requisição e revisão própria.

A versão modificada de lz-string preserva sua licença MIT em app/LICENSE_LZ_STRING. O único ajuste de algoritmo adiciona limites opcionais à descompressão; a compatibilidade dos saves normais é testada.

## Validação

`node tools/test-security.cjs` verifica cargas maliciosas e casos válidos. `node tools/test-game.cjs` verifica temporadas, carreiras e saves. `node tools/test-edition.cjs` verifica os presets e históricos. Os testes não substituem revisão manual.

Para manutenção, não publique credenciais ou dados pessoais em issues. Antes de atualizar dependências, confira origem, licença e compatibilidade offline. Mantenha a conta GitHub protegida e revise permissões e alterações antes de publicar.
