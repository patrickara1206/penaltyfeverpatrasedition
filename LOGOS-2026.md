# Escudos e identidades de competições — consulta em 29/10/2026

O catálogo usa arquivos locais e inclui suas fontes em `app/logos-manifest.json`. A mesma imagem é usada no site e no pacote offline. O carregamento do jogo não depende dos sites de origem.

Foram revisadas 748 entradas de clubes e 54 identidades de competições nesta atualização. As edições históricas das Copas mantêm o emblema ou cartaz correspondente ao ano da competição. A data de consulta não significa que toda marca tenha sido redesenhada em 2026.

Fontes consultadas: diretórios oficiais SAFF 2026/27, AUF 2026, Difutbol Primera C 2026, FEF Ascenso Nacional 2026 e tabelas LigaPro 2026; os demais arquivos têm referências ao catálogo FootyLogos, Football Logos ou à página identificada do clube.

## Cobertura e pendências

1630 de 1752 nomes de equipes das competições atuais possuem imagem identificada. Restam 122 monogramas de reserva e três competições sem identidade confirmada: Segunda Categoría do Equador e Second Division A/B do Egito. Nenhum desses monogramas deve ser apresentado como escudo oficial.

Parte das fontes de clubes amadores não publica imagem; os diretórios da EFA e Diski Zone também recusaram as consultas automatizadas (HTTP 403). Clubes homônimos, filiais sem vínculo confirmado e mudanças de identidade não documentadas permaneceram pendentes. Não foram atribuídos escudos de outro clube apenas pela semelhança do nome.

A lista exata de pendências fica em `app/logo-audit-current.json`, e as fontes reproduzíveis em `tools/logo-sources-2026.json`.

## Reprodução

O importador exige Python com Pillow. Ele valida imagens, mantém o arquivo anterior se a origem falhar e aplica limite de dimensão de 384 px. A conversão WebP é sem perdas; a transparência existente é preservada. Não remove elementos brancos que façam parte do arquivo original.

```text
python tools/import-logo-sources.py tools/logo-sources-2026.json
python tools/optimize-logo-assets.py
python tools/embed-logos.py
node tools/test-embedded-logos.cjs
python tools/test-visual-assets.py
python tools/build-cloudflare.py dist-cloudflare
```

Não há certificação de atualização oficial de 2026 para todos os arquivos. A cobertura incompleta está registrada para não confundir imagem identificada, marca confirmada pelo organizador e emblema de reserva.
