### Implementação de Cluster de Motivos de Tickets

Objetivo:
Criar uma camada de **normalização e agrupamento de motivos de tickets** para melhorar o diagnóstico operacional exibido no painel de retenção. O sistema atualmente apresenta motivos individuais (ex.: "INDISPONIBILIDADE", "DESCONTO DE INDISPONIBILIDADE", "CONFIGURAÇÃO"), o que pode gerar interpretações equivocadas, pois diferentes tipos de tickets representam naturezas distintas de interação com o cliente.

A implementação deve introduzir  **clusters de motivos** , permitindo agrupar tickets em categorias operacionais maiores, como problemas técnicos, questões administrativas ou financeiras.

---

### 1. Conceito

Os motivos individuais de tickets serão mapeados para um  **cluster funcional** .

Exemplo:

Motivos individuais:

* INDISPONIBILIDADE
* LENTIDÃO
* CONFIGURAÇÃO
* DESCONTO DE INDISPONIBILIDADE
* SEGUNDA VIA DE BOLETO

Clusters:

* TECNICO
* ADMINISTRATIVO
* FINANCEIRO
* COMERCIAL
* OUTROS

Assim, a análise deixa de depender de textos específicos e passa a refletir  **a natureza do problema** .

---

### 2. Fonte dos dados

Os motivos dos tickets atualmente são obtidos a partir de campos do Atrix, principalmente:

* `tbltickettyperequest.title`
  ou
* `tbltickets.title`

Esses campos não foram projetados para analytics e podem conter grande variabilidade textual. Por esse motivo, a classificação deve ser implementada como  **uma camada de mapeamento controlado no código** , não diretamente no banco.

---

### 3. Estrutura do mapeamento

Criar um dicionário de classificação centralizado, por exemplo:

```python
MOTIVO_CLUSTER_MAP = {
    "INDISPONIBILIDADE": "TECNICO",
    "LENTIDÃO": "TECNICO",
    "OSCILAÇÃO": "TECNICO",
    "CONFIGURAÇÃO": "TECNICO",
    "FALHA DE LINK": "TECNICO",

    "DESCONTO DE INDISPONIBILIDADE": "ADMINISTRATIVO",
    "ANÁLISE DE DESCONTO": "ADMINISTRATIVO",

    "SEGUNDA VIA DE BOLETO": "FINANCEIRO",
    "FATURA": "FINANCEIRO",
    "PAGAMENTO": "FINANCEIRO",

    "UPGRADE": "COMERCIAL",
    "DOWNGRADE": "COMERCIAL"
}
```

Qualquer motivo não encontrado nesse mapeamento deve cair em:

```
OUTROS
```

---

### 4. Aplicação da classificação

Após carregar os tickets no DataFrame:

```python
df["cluster_motivo"] = df["motivo"].map(MOTIVO_CLUSTER_MAP).fillna("OUTROS")
```

Isso cria uma nova coluna normalizada para análise.

---

### 5. Agregação para diagnóstico

A distribuição de clusters deve ser calculada para a janela de análise (ex.: 90 dias):

```python
df_clusters = (
    df.groupby("cluster_motivo")
    .size()
    .sort_values(ascending=False)
)
```

Resultado esperado:

```
TECNICO..............14
ADMINISTRATIVO.......3
FINANCEIRO...........1
```

---

### 6. Integração com o painel

Adicionar uma nova seção no diagnóstico:

```
Distribuição de Tickets (90d)

Técnicos..............14
Administrativos.......3
Financeiros...........1
Outros................0
```

Essa visão deve complementar:

* Top Motivos
* SLA
* Classificações de encerramento

---

### 7. Uso futuro

Essa classificação também poderá ser utilizada para:

* cálculo de **score de churn**
* identificação de **incidentes recorrentes**
* detecção de **padrões operacionais por cliente**
* criação de **alertas automáticos**

Exemplo:

```
Se cluster TECNICO > 5 nos últimos 30 dias
→ aumentar risco de churn
```

---

### 8. Requisitos técnicos

1. Implementação no  **service layer** , não na camada de UI.
2. O mapeamento deve ser mantido em  **estrutura centralizada e facilmente extensível** .
3. A lógica deve ser independente de idioma ou variações de caixa (normalizar texto antes da comparação).
4. A classificação deve ocorrer  **antes das agregações usadas no dashboard** .

---

### Resultado esperado

Com essa camada de clusterização, o painel deixa de analisar apenas **textos de tickets** e passa a trabalhar com  **categorias operacionais estruturadas** , permitindo diagnósticos mais confiáveis para a célula de retenção.
