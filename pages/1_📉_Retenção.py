import streamlit as st
import pandas as pd
import base64
import os

from services.retencao_service import RetencaoService

def format_currency(value):
    if value is None:
        return "R$ 0,00"
    return f"R$ {value:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

def get_base64_svg(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

st.set_page_config(page_title="Retenção de Clientes", layout="wide", initial_sidebar_state="collapsed", page_icon="assets/favicon.png")

# Headline com Logo (HTML customizado para alinhamento perfeito)
logo_b64 = get_base64_svg("assets/retencao.png")
st.markdown(
    f"""
    <div style="display: flex; align-items: flex-end; gap: 15px; margin-bottom: 20px;">
        <img src="data:image/png;base64,{logo_b64}" width="55" style="margin-bottom: 5px;">
        <h1 style="margin: 0; padding: 0; font-size: 2.6rem; line-height: 1.2;">Retenção de Clientes</h1>
    </div>
    """,
    unsafe_allow_html=True
)
st.divider()

# ==============================
# BUSCA
# ==============================

cnpj = st.text_input("Buscar cliente por CNPJ")

from configs.mapping import formatar_cnpj

if not cnpj:
    st.stop()
    
cnpj_formatado = formatar_cnpj(cnpj)

painel = RetencaoService.get_painel_cliente(cnpj_formatado)

if not painel:
    st.warning("Cliente não encontrado")
    st.stop()

cliente = painel["cliente"]

# ==============================
# CLIENTE (COMPACTO)
# ==============================

segmento = cliente['segmento_nome'] if cliente.get('segmento_nome') else cliente['segmentid']

st.markdown(
    f"""
**Cliente:** {cliente['companyname']}  
**Segmento:** 
<span style="
background-color:#1f6feb;
color:white;
padding:3px 10px;
border-radius:8px;
font-size:14px;
font-weight:600;
">
{segmento}
</span>
""",
    unsafe_allow_html=True
)

st.divider()

# ==============================
# SERVIÇOS DO CLIENTE
# ==============================

st.subheader("Serviços do Cliente")

servicos = painel["servicos"]

if not servicos:
    st.info("Este cliente não possui serviços cadastrados.")
    st.stop()

df_servicos = pd.DataFrame(servicos)
if not df_servicos.empty:
    df_servicos["servico_id"] = df_servicos["servico_id"].astype(int)

df_servicos_view = df_servicos[[
    "saude",
    "servico_id",
    "designador",
    "plano",
    "domainstatus",
    "tecnologia",
    "velocidade",
    "cidade",
    "valor",
    "regdate"
]]

df_servicos_view = df_servicos_view.rename(columns={
    "saude": "Saúde",
    "servico_id": "Serviço",
    "designador": "Designador",
    "plano": "Plano",
    "domainstatus": "Status",
    "tecnologia": "Tecnologia",
    "velocidade": "Velocidade",
    "cidade": "Cidade",
    "valor": "Valor",
    "regdate": "Ativado"
})

df_servicos_view["Serviço"] = df_servicos_view["Serviço"].astype(str)
df_servicos_view["Valor"] = df_servicos_view["Valor"].apply(format_currency)

# tabela selecionável de serviços (seleção nativa do Streamlit)

# instrução visual para seleção
st.caption("⬅️ Selecione o serviço clicando na linha")

# tabela selecionável de serviços (seleção nativa do Streamlit)

event = st.dataframe(
    df_servicos_view,
    use_container_width=True,
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row",
)

# determinar qual linha foi selecionada
if event.selection.rows:
    selected_index = event.selection.rows[0]
    servico_id = int(df_servicos.iloc[selected_index]["servico_id"])
else:
    # padrão: primeiro serviço
    servico_id = int(df_servicos.iloc[0]["servico_id"])

painel = RetencaoService.get_painel_cliente(cnpj_formatado, servico_id)

servico = painel["servico_selecionado"]

st.divider()

# ==============================
# SERVIÇO SELECIONADO
# ==============================

st.subheader("Serviço Selecionado")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.write("Plano")
    st.write(f"**{servico['plano']}**")

with col2:
    st.write("Valor")
    st.write(f"**{format_currency(servico['valor'])}**")

with col3:
    st.write("Status")
    st.write(f"**{servico['domainstatus']}**")

with col4:
    st.write("Ativado em")
    st.write(f"**{servico['regdate']}**")


descontos = servico.get("descontos", [])
total_desconto = servico.get("total_desconto", 0)

if descontos:
    st.write("")
    with st.expander(f"🏷️ Histórico de Descontos (Concedido: {format_currency(total_desconto)})"):
        df_desc = pd.DataFrame(descontos)
        
        # Formatações Visuais
        df_desc["value"] = df_desc["value"].apply(lambda v: format_currency(v) if pd.notnull(v) else format_currency(0))
        if "datebegin" in df_desc.columns:
            df_desc["datebegin"] = pd.to_datetime(df_desc["datebegin"]).dt.strftime("%d/%m/%Y").fillna("-")      
        if "dateend" in df_desc.columns:
            df_desc["dateend"] = pd.to_datetime(df_desc["dateend"]).dt.strftime("%d/%m/%Y").fillna("-")
            
        df_desc_view = df_desc.rename(columns={
            "description": "Descrição",
            "category": "Categoria",
            "value": "Valor",
            "datebegin": "Início",
            "dateend": "Fim"
        })
        
        # Ocultar colunas internas
        colunas_exibir = ["Descrição", "Categoria", "Valor", "Início", "Fim"]
        st.dataframe(df_desc_view[colunas_exibir], use_container_width=True, hide_index=True)

st.divider()

# ==============================
# DIAGNÓSTICO + FINANCEIRO
# ==============================

diagnostico = painel["diagnostico"]
financeiro = painel["financeiro"]

col_diag, col_fin = st.columns(2)

# ---------- Diagnóstico ----------

with col_diag:

    st.subheader("Diagnóstico")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Tickets 30 dias",
            diagnostico["tickets_30d"]
        )

    with c2:
        st.metric(
            "Tickets 90 dias",
            diagnostico["tickets_90d"]
        )

    with c3:
        st.metric(
            "Total Tickets",
            diagnostico["total_tickets"]
        )

# ---------- Financeiro ----------

with col_fin:

    st.subheader("Financeiro")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Faturas abertas",
            financeiro["faturas_abertas"]
        )

    with c2:
        st.metric(
            "Valor em aberto",
            format_currency(financeiro['valor_aberto'])
        )

    with c3:
        st.metric(
            label="Última fatura",
            value=str(financeiro["ultima_fatura"]) if financeiro["ultima_fatura"] else "-",           
        )

st.divider()

# ==============================
# HISTÓRICO DE TICKETS
# ==============================
# --- ANÁLISE DE SUPORTE E TICKETS ---
st.markdown("### 🎫 Análise de Suporte e Tickets")

# 1. Camada 1: Mini Diagnóstico Automático
mini_diag = diagnostico.get("mini_diagnostico") if diagnostico else None
if mini_diag:
    if "Crítico" in mini_diag:
        st.error(mini_diag)
    else:
        st.warning(mini_diag)
else:
    st.info("✅ **Normal:** Volume de tickets recentes do cliente está dentro da normalidade para este serviço.")

# 2. Camada 2: Scorecards Sintéticos
col_motivos, col_sla, col_encerramento, col_clusters = st.columns(4)

with col_motivos:
    st.markdown("#### Top Motivos (90d)")
    motivos = diagnostico.get("motivos_90d", []) if diagnostico else []
    if motivos:
        for m in motivos:
            st.markdown(f"- **{m['motivo'][:35].strip()}**: {m['total']}")
    else:
        st.markdown("- Sem dados recentes")

with col_clusters:
    st.markdown("#### Distribuição (90d)")
    clusters_lst = diagnostico.get("clusters_90d", []) if diagnostico else []
    if clusters_lst:
        for c in clusters_lst:
            st.markdown(f"- **{c['cluster']}**: {c['total']}")
    else:
        st.markdown("- Sem dados recentes")

with col_sla:
    st.markdown("#### SLA de Resolução (90d)")
    if diagnostico and diagnostico.get("sla_90d"):
        sla = diagnostico["sla_90d"]
        st.metric("SLA Médio", sla.get("sla_medio_horas", "-"))
        st.metric("Pior SLA", sla.get("sla_max_horas", "-"))
        st.metric("% Resolv. < 24h", sla.get("resolvidos_24h_pct", "-"))
    else:
        st.markdown("- Sem dados recentes")

with col_encerramento:
    st.markdown("#### Classificações (90d)")
    encerrados = diagnostico.get("encerrados_90d", []) if diagnostico else []
    if encerrados:
        for e in encerrados:
            st.markdown(f"- **{e['classificacao'][:25]}**: {e['total']}")
    else:
        st.markdown("- Sem dados recentes")

st.markdown("---")
st.markdown("#### Histórico Operacional (Analítico)")

tickets = painel["tickets"]

if not tickets:
    st.info("Nenhum ticket encontrado para este serviço.")
else:
    df_tickets = pd.DataFrame(tickets)
    df_tickets["id"] = df_tickets["id"].astype(int)

    # Gráfico Temporal de Tickets
    with st.expander("📊 Evolução Mensal de Incidentes (12 meses)", expanded=False):
        evolucao = diagnostico.get("evolucao_12m", []) if diagnostico else []
        if evolucao:
            df_chart = pd.DataFrame(evolucao)
            # Ordena pelo campo mes_ordem já agrupado (YYYY-MM)
            df_chart = df_chart.sort_values(by="mes_ordem")
            
            # Redefine o index para mes_nome (MM/YYYY) e plota o total
            df_chart = df_chart.set_index("mes_nome")
            st.bar_chart(df_chart["total"], use_container_width=True)
        else:
            st.info("Não há dados de volumetria suficientes nos últimos 12 meses.")

    st.markdown("#### Histórico Operacional (Analítico)")

    df_tickets_view = df_tickets[[
        "id",
        "cluster",
        "tid",
        "motivo",
        "title",
        "status",
        "date",
        "dateclosed",
        "sla_horas",
        "departamento",
        "classificacao"
    ]].copy()

    # Criar coluna de link para o Atrix
    base_url = "https://atrix.mobtelecom.com.br/controle/addonmodules.php?module=helpdesk#/app/ticket/"
    df_tickets_view["id_link"] = df_tickets_view["id"].apply(lambda x: f"{base_url}{x}")

    df_tickets_view = df_tickets_view.rename(columns={
        "id": "Ticket ID",
        "cluster": "Natureza",
        "tid": "Protocolo",
        "motivo": "Motivo",
        "title": "Título",
        "status": "Status",
        "date": "Abertura",
        "dateclosed": "Fechamento",
        "sla_horas": "SLA",
        "departamento": "Departamento",
        "classificacao": "Encerramento"
    })

    st.dataframe(
        df_tickets_view,
        use_container_width=True,
        hide_index=True,
        column_order=("Ticket ID", "id_link", "Protocolo", "Natureza", "Departamento", "Motivo", "Título", "Status", "Abertura", "Fechamento", "SLA", "Encerramento"),
        column_config={
            "id_link": st.column_config.LinkColumn(
                "Link Atrix",
                help="Clique para abrir o ticket no Atrix",
                validate="^https://.*",
                max_chars=100,
                display_text="Abrir ticket"
            ),
            "Ticket ID": st.column_config.NumberColumn("Ticket ID", format="%d")
        }
    )
