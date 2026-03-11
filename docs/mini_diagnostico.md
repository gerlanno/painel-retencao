Os critérios do **Mini-Diagnóstico Automático** que implementamos foram pensados exclusivamente focados em **Retenção** (ou seja, identificar a probabilidade de um cliente cancelar um serviço por problemas técnicos acumulados recentemente).

A lógica funciona com os seguintes pilares, cruzando o **Volume Recente (30 dias)** com a  **Tendência de Problemas (90 dias)** :

### 1. Gatilho de Ativação (Tickets Curtos - 30 dias)

O diagnóstico só "apita" se o cliente teve transtornos em um período muito curto.

* **Se tiver 0 ou 1 ticket (Últimos 30 dias):** O sistema considera saudável. O método retorna em branco e a tela exibe o banner verde: *"✅ Normal: Volume de tickets recentes do cliente está dentro da normalidade..."*
* **Se tiver 2 ou mais tickets:** O sistema aciona os alertas, pois entende que reabrir chamados na mesma competência é um indicativo de frustração crescente do cliente B2B.

### 2. Níveis de Risco (Severidade)

Quando os alertas são acionados, o sistema classifica em duas bandas:

* 🟡 **Nível Atenção (2 a 3 tickets):** O alerta gerado é mapeado como  *"instabilidade recorrente"* . Serve para avisar o analista que a experiência do cliente com o serviço não está legal neste mês.
* 🔴 **Nível Crítico (4 tickets ou mais):** O alerta gerado é mapeado abertamente como  *"alto risco de churn"* . 4 incidentes em menos de 30 dias estatisticamente representam uma quebra severa de SLA que precede pedidos de rescisão contratual.

### 3. Identificação da Raiz do Problema

Sempre que um alerta é gerado (seja Atenção ou Crítico), a inteligência do mini-diagnóstico olha para a tabela de `Motivos`. Ele captura o **Motivo Número 1 (o mais frequente)** listado nos tickets dos últimos 90 dias.

A ideia é entregar a resposta pronta mastigada na cara do analista, resultando nas frases que você viu:

> *"🚨 **Atenção:** Instabilidade recorrente. Cliente abriu 2 tickets nos últimos 30 dias. Principal motivo reportado: 'Oscilação'."*

> *"🚨 **Crítico:** Alto risco de churn. Cliente abriu 5 tickets nos últimos 30 dias. Principal motivo reportado: 'Queda de conexão'."*

Essa lógica inteira vive dentro da função

![](vscode-file://vscode-app/c:/Users/gerlanno.silva/AppData/Local/Programs/Antigravity/resources/app/extensions/theme-symbols/src/icons/files/python.svg)

_gerar_mini_diagnostico que colocamos no backend (![](vscode-file://vscode-app/c:/Users/gerlanno.silva/AppData/Local/Programs/Antigravity/resources/app/extensions/theme-symbols/src/icons/files/python.svg)

RetencaoService), então é muito fácil para você calibrar as réguas depois se perceber que para o seu negócio B2B, o risco vermelho deve disparar com 3 ou com 5 chamados.
