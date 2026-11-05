# Na Marca · v1.0.9

Decisões nos pênaltis, temporadas e carreira, construídas sobre a partida aprovada da v1.0.6. A identidade do site usa verde, azul, amarelo e branco.

[Jogar online](https://penaltyfeverpatras.pages.dev/) · [Release v1.0.9](https://github.com/patrickara1206/penaltyfeverpatrasedition/releases/tag/v1.0.9) · [Baixar ZIP portátil](https://github.com/patrickara1206/penaltyfeverpatrasedition/releases/download/v1.0.9/Na-Marca-v1.0.9.zip)

## Jogar sem instalação

1. Extraia o ZIP inteiro.
2. Abra JOGAR.html em navegador moderno com JavaScript e WebAssembly.
3. Use o botão ABRIR O JOGO caso o redirecionamento automático seja bloqueado.

Não precisa de Flash instalado, terminal ou administrador. O modo offline inclui seus recursos e uma agenda datada; a agenda ao vivo exige a versão online. Políticas de computadores administrados e navegadores antigos podem limitar a execução. Não existe garantia de compatibilidade ou desempenho em todo computador.

Exporte os saves antes de mudar de navegador ou computador. Os identificadores de armazenamento anteriores foram preservados; o jogo não sincroniza saves pela internet.

## Novidades e cobertura

Consulte [RELEASE-v1.0.9.md](RELEASE-v1.0.9.md) e [DADOS-v1.0.9.md](DADOS-v1.0.9.md). Foram incluídos 438 elencos de clubes, 209 ordens documentadas, 489 participações nas Copas históricas, 88 elencos de seleções recentes, sete fotografias de troféus e consulta à agenda real de 17 competições. Os clubes sem confirmação mostram cobradores genéricos. Competições adaptadas e imagens de contingência permanecem identificadas. Esta edição não certifica cobertura oficial integral de todas as equipes ou regulamentos.

## Desenvolvimento e testes

O site é estático. Para desenvolvimento, sirva a pasta app com um servidor local. A publicação web é construída com `python tools/build-cloudflare.py dist-cloudflare`; o pacote portátil, com `python tools/package-release.py`.

Os testes da release incluem física original byte a byte, animação da torcida, cores, ponte Ruffle/resultados, playoffs entre divisões, saves, imagens incorporadas, elencos por edição e carregamento WebAssembly. A validação automatizada não equivale a testar todos os computadores ou provar ausência de todo bug.

## Créditos e fontes

Motor e parte dos gráficos, animações e áudio: Penalty Fever Plus, FlashFooty / Vladeta M. (2009). A identidade Na Marca e os painéis desta edição são próprios; não há declaração de licença comercial do clássico.

Ruffle 0.7.1: Apache 2.0/MIT, em app/LICENSE_APACHE e app/LICENSE_MIT. lz-string 1.5.0, pieroxy: MIT, em app/LICENSE_LZ_STRING. World Cup Database: Joshua C. Fjelstul, CC BY-SA 4.0, em licenses/worldcup/NOTICE.md. Fotografias dos troféus: autoria e licença nos cartões e em licenses/trophy-photos.json. Escudos: [LOGOS.md](LOGOS.md) e app/logos-manifest.json.
