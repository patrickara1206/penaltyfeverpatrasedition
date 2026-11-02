# Hospedagem

Site atual: https://penaltyfeverpatras.pages.dev/

Cloudflare Pages, projeto `penaltyfeverpatras`, repositório `patrickara1206/penaltyfeverpatrasedition`.

- Produção: branch `v1.0.6`, deploy automático habilitado.
- Preview: `None` (deploys automáticos de outras branches desativados).
- Build: `python3 tools/build-cloudflare.py dist-cloudflare`.
- Diretório publicado: `dist-cloudflare`.
- Beta `v1.0.7`: somente GitHub. Não alterar a branch de produção para a beta. Usar também o prefixo `[CF-Pages-Skip]` nos commits da beta como proteção adicional contra publicação acidental por integração Git.

A alteração do controle de branches não muda a versão já servida: um novo commit na branch de produção inicia o deploy seguinte. Conferir o commit e o estado de produção no painel e verificar `index.html` e `match.swf` no endereço público.

O Worker antigo e o endereço anterior do GitHub Pages têm configuração independente. Não reescrever tags, não forçar push e não trocar o subdomínio geral da conta Cloudflare.

Os saves pertencem ao navegador e à origem. Exporte e importe o save ao mudar de endereço. O código não envia saves ao provedor.

As releases usam o token temporário do GitHub Actions, com `contents:write`. Nenhum token do Cloudflare integra o código ou o pacote. Os arquivos portáteis são validados por CRC, relação de arquivos e SHA256 antes de publicação.
