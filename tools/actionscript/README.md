# Rótulos incorporados

physics.as é o código AS2 da física corrigida. physics-actions.bin foi compilado por JPEXS FFDec 26.3.0 (importScript no frame_106 do SWF original).

text-labels.bin contém 30 bitmaps com os textos dos dez idiomas; text-labels.json registra os textos/fontes/dimensões. O builder injeta esses recursos no SWF, sem requisições de fonte em execução.

Para regenerar os textos, use tools/build-text-labels.py --fonts DIRETORIO_DAS_FONTES. Requer Pillow, uharfbuzz e freetype-py apenas para o build. Fontes: Noto Sans, Noto Sans SC, Noto Naskh Arabic e Noto Sans Devanagari do repositório google/fonts (ofl); licenças em licenses/noto. Depois execute tools/build_match.py e tools/embed_data.py. O jogo distribuído não precisa de Python ou dessas bibliotecas.
