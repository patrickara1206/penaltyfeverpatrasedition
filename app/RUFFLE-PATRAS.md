# Adaptação local do Ruffle

Os arquivos core.ruffle.*.js mantêm as licenças MIT/Apache distribuídas no pacote. A função de despacho ExternalInterface foi adaptada para aceitar apenas os cinco callbacks patrasReady, patrasTurn, patrasShot, patrasProgress e patrasResult. A implementação original usava new Function, incompatível com a CSP desta edição; a adaptação chama diretamente as funções conhecidas, sem interpretar código enviado pelo SWF. Os hashes no carregador correspondem aos módulos modificados.

O restante do runtime e a jogabilidade do SWF foram preservados.
