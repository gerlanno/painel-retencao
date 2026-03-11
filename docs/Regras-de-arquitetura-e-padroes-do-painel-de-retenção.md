### Regras de Arquitetura e Padrão de Desenvolvimento do Painel de Retenção

Objetivo:
Garantir que toda nova funcionalidade implementada no painel de retenção siga  **o mesmo padrão arquitetural já adotado no projeto** , evitando mistura de responsabilidades entre camadas e mantendo o código organizado, previsível e extensível.

O projeto já segue uma arquitetura em camadas:

```
queries → repositories → services → UI (Streamlit)
```

Todas as novas implementações devem respeitar rigorosamente essa separação.

---

## 1. Separação de responsabilidades

### Camada de Queries

Responsável  **exclusivamente por SQL** .

Regras:

* Conter apenas consultas SQL.
* Não deve haver lógica de negócio.
* Não deve haver transformação de dados.
* Não deve conter lógica condicional ou regras operacionais.

Exemplo de responsabilidade:

* buscar tickets do serviço
* buscar classificações
* buscar dados financeiros
* buscar motivos de tickets

Resultado esperado:

```
DataFrame ou lista de registros brutos do banco
```

---

### Camada de Repositories

Responsável por  **executar queries e retornar dados estruturados** .

Regras:

* Executa SQL definido na camada de queries.
* Converte resultados para DataFrame ou estruturas Python.
* Pode realizar ajustes simples de formatação de dados.
* Não deve conter lógica de negócio complexa.

Exemplo:

```
TicketRepository.get_tickets_by_service(service_id)
```

Essa camada apenas entrega os dados.

---

### Camada de Services

Responsável por  **toda lógica de negócio e transformação analítica** .

Regras:

* Toda regra operacional deve estar aqui.
* Nenhuma regra analítica deve estar na UI.
* Nenhum cálculo deve ocorrer diretamente na interface Streamlit.

Exemplos de responsabilidades desta camada:

* cálculo de SLA médio
* cálculo de pior SLA
* cálculo de tickets em janelas de tempo (30d / 90d)
* clusterização de motivos
* cálculo de score de churn
* agregações para diagnóstico
* normalização de dados

Exemplo:

```
RetencaoService.build_ticket_diagnosis(service_id)
```

Essa função deve retornar  **dados já prontos para exibição** .

---

### Camada de UI (Streamlit)

Responsável  **somente pela renderização da interface** .

Regras:

* Não deve conter regras de negócio.
* Não deve executar SQL.
* Não deve conter lógica de classificação.
* Deve apenas consumir dados produzidos pela camada de services.

Exemplo de uso correto:

```
diagnostico = retencao_service.get_ticket_diagnosis(service_id)

st.metric("SLA médio", diagnostico["sla_medio"])
st.metric("Pior SLA", diagnostico["pior_sla"])
```

A UI apenas apresenta dados.

---

## 2. Regra fundamental do projeto

Sempre seguir o fluxo:

```
Banco
↓
Query
↓
Repository
↓
Service
↓
UI
```

Nunca pular camadas.

Exemplos proibidos:

❌ UI executando SQL
❌ UI calculando métricas
❌ Repository contendo regras de negócio
❌ Query contendo lógica analítica

---

## 3. Estrutura esperada para novas funcionalidades

Toda nova funcionalidade deve ser implementada seguindo este padrão:

```
queries/
    tickets_queries.py

repositories/
    ticket_repository.py

services/
    ticket_analysis_service.py
```

Exemplo aplicado ao cluster de motivos:

```
query → busca motivos dos tickets
repository → retorna DataFrame
service → aplica clusterização e agregação
UI → apenas exibe resultado
```

---

## 4. Dados retornados pelos Services

Os services devem retornar  **dados já consolidados para a UI** .

Exemplo de estrutura retornada:

```
{
    "top_motivos": [...],
    "sla_medio": 20,
    "pior_sla": 53,
    "clusters_motivos": {
        "TECNICO": 14,
        "ADMINISTRATIVO": 3,
        "FINANCEIRO": 1
    }
}
```

A interface não deve precisar calcular nada.

---

## 5. Centralização de regras

Qualquer regra operacional deve existir  **em apenas um lugar** .

Exemplos:

* mapeamento de cluster de motivos
* cálculo de SLA
* cálculo de risco de churn
* regras de classificação

Isso evita duplicação de lógica no sistema.

---

## 6. Normalização de dados

Antes de qualquer análise:

* normalizar caixa de texto (upper/lower)
* remover variações triviais de texto
* padronizar valores nulos

Isso deve ocorrer  **na camada de service** .

---

## 7. Evolução futura

A arquitetura adotada permite evolução sem quebrar a interface.

Exemplos de melhorias futuras que devem seguir o mesmo padrão:

* score de churn baseado em múltiplos fatores
* detecção automática de incidentes recorrentes
* cálculo de MTBF do serviço
* análise temporal de tickets
* recomendação automática de retenção

Todas essas regras devem ser implementadas  **no service layer** .

---

## Resultado esperado

Seguindo esse padrão:

* o código permanece organizado
* novas funcionalidades não quebram a UI
* a lógica analítica fica centralizada
* o sistema continua evoluindo sem gerar acoplamento indevido entre camadas
