# Código e reprodução dos testes

Para jogar, basta abrir JOGAR.html. Não é necessário instalar ferramentas.

- app/app.js: interface, temporadas, áudio, abandono e persistência.
- app/engine.js: tabelas, fases, mata-mata e playoffs.
- app/football.js: elencos fictícios, uniformes e dificuldade.
- app/career.js: mundo, calendário, propostas, títulos e divisões.
- app/career-ui.js: perfil, central do técnico, mundo e relatórios.
- app/storage.js: compressão e leitura dos saves.
- app/data.json: participantes e fontes. app/data.js: dados e SWF embutidos para arquivo local.
- app/wasm-local.js: dois módulos WebAssembly do Ruffle embutidos.
- tools/build_match.py: adaptação AVM1 do SWF original; tools/embed_data.py: atualiza os dados embutidos.

Para reconstruir dados ou SWF, Python3 (opcional):

```
python tools/build_match.py
python tools/embed_data.py
```

Para executar os testes de lógica, Node24 (opcional, sem dependências npm):

```
node tools/test-game.cjs
```

O teste gera VALIDACAO.json. A verificação visual usa um navegador e não está automatizada pelo script de lógica. Leia as limitações do relatório.

Ruffle0.7.1 self-hosted e lz-string1.5.0 são distribuições oficiais com licenças preservadas. Os nomes internos pp_ e PatrasEngine identificam a ponte de código antiga; a marca pública é PF.

Assets visuais: app/logos-manifest.json e app/logos.js associam as imagens em app/assets/logos. tools/stadium_art.py desenha arquibancada e placas nativas do SWF; tools/build_match.py aplica cores após cada quadro e mantém os indicadores de cobranças. A validação estrutural e das imagens é reproduzível com `python tools/test-visual-assets.py`, usando apenas Python3, sem bibliotecas extras.
