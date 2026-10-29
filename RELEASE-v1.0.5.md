# v1.0.5 — animações, acessibilidade e publicação

Extraia o ZIP inteiro e abra JOGAR.html. Não requer instalação ou administrador.

- Pele e cabeça do cobrador restauradas após cada troca de quadro; camisa e cabelo do goleiro reaplicados em todos os quadros de defesa.
- Decisão lateral do gol usa a posição da bola, não a coordenada integrada da sombra. Bola segurada, voltando para o campo, fora das laterais ou acima do travessão não marca gol nessa verificação.
- Tela cheia usa a API do Ruffle em todos os modos que compartilham a sessão de partida.
- Animação após a cobrança reduzida de 130 para 75 quadros por padrão (40 FPS); opções de 75, 110 e 130 nas configurações. A velocidade física do chute mantém a dificuldade escolhida.
- Aba Configurações com tamanho de texto 100–150%, alto contraste, redução de movimento e três modos de visão de cores. Cobranças ganham marcas de acerto/erro além da cor.
- Navegação e mensagens principais em português, inglês, espanhol, francês, alemão, italiano, chinês, árabe, hindi e russo. Avisos de cobrança e número da rodada também mudam dentro do Flash. Textos documentais, históricos e parte das telas secundárias permanecem no idioma original; a tradução integral ainda não está concluída.
- Arte original de estádio e bola criada por IA para a tela inicial. Removido “Exibição VS” da partida rápida.
- 627 escudos atualizados por correspondência exata de nomes no catálogo football-logos.cc, consultado em 29/10/2026. Auditoria em app/logo-audit-v105.json. Permanecem 708 monogramas não verificados entre equipes atuais; não é uma coleção integral de marcas oficiais de 2026. Logos de competições existentes mantidas, com imagens incorporadas para uso offline.
- Runtime WASM dividido em seis arquivos, preservando os bytes dos dois módulos, para respeitar o limite por arquivo do Cloudflare. Bundle público contém só recursos do jogo, sem ferramentas e saves.

## Validação

Oito cenários de decisão de gol; validação WebAssembly dos dois módulos reconstruídos; testes de segurança, bridge de resultados, arquivos de imagens e logos incorporadas. Testes no navegador confirmam início da partida, mensagens em inglês, rodada traduzida, tela cheia do Ruffle e cores de corrida/defesa. O motor visual ainda exige mouse/apontador; não é um jogo inteiramente acessível por leitor de tela.

## Estado da edição

Prévia: mantém os recortes de catálogo e adaptações de formato documentados na v1.0.4. Motor e gráficos originais derivados de Penalty Fever Plus / FlashFooty, emulados por Ruffle; marcas pertencem aos respectivos titulares. Não há alegação de licenciamento oficial.
## Fontes e idiomas no Flash

Os 30 rótulos de cobrança/defesa/rodada dos dez idiomas são compostos com Noto e HarfBuzz e incorporados como bitmaps pequenos no SWF. Isso evita caracteres ausentes nas fontes padrão do Ruffle, inclusive chinês, árabe e hindi. Não há download de fontes durante a partida. Licenças SIL OFL em licenses/noto. O tamanho desses avisos acompanha a preferência de letras.

Teste adicional no navegador: caracteres chineses e árabes, além de uma partida rápida completa com tela de resultado e retorno à seleção.
