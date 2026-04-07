import streamlit as st
import pandas as pd
import io
from queries.db_connections import get_atrix_connection

st.set_page_config(page_title="Serviços e Tickets", layout="wide", page_icon="📊")

st.markdown("## 📊 Serviços e Tickets por Cliente")
st.divider()

# Campo de texto para buscar outro ID, com o 6971 como padrão default
cliente_id_input = st.text_input("Buscar por ID do Cliente", value="6971")

if not cliente_id_input:
    st.info("Informe um ID de cliente para analisar.")
    st.stop()

query_path = "queries/serv_e_tickets_por_clientes.sql"

def load_data(cliente_id):
    try:
        with open(query_path, 'r', encoding='utf-8') as file:
            query = file.read()
            
        conn = get_atrix_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (cliente_id,))
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados
    except Exception as e:
        st.error(f"Erro ao executar a consulta: {e}")
        return None

query_tickets_path = "queries/tickets_por_cliente.sql"

def load_tickets_data(cliente_id):
    try:
        with open(query_tickets_path, 'r', encoding='utf-8') as file:
            query = file.read()
            
        conn = get_atrix_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (cliente_id,))
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados
    except Exception as e:
        st.error(f"Erro ao executar a consulta de tickets: {e}")
        return None

# Spinner nativo para indicar carregamento
with st.spinner("Carregando dados..."):
    dados = load_data(cliente_id_input)

if dados is not None:
    if len(dados) == 0:
        st.warning(f"Nenhum serviço/ticket encontrado para o cliente de ID: {cliente_id_input}.")
    else:
        df = pd.DataFrame(dados)
        st.success(f"Busca finalizada! {len(dados)} registro(s) encontrado(s).")
        
        st.markdown("### Serviços")
        
        # O text overflow padrão pode esconder algumas coisas, mas o st.table força a montagem da tabela no HTML.
        event = st.dataframe(
            df, 
            use_container_width=True, 
            on_select="rerun",
            selection_mode="single-row",
            column_config={"SERVIÇO": st.column_config.NumberColumn("SERVIÇO", format="%d"), "NUMERO": st.column_config.NumberColumn("NUMERO", format="%d")}
        )

        buffer = io.BytesIO()
        df.to_excel(buffer, index=False)
        
        st.download_button(
            label="📥 Exportar Serviços para Excel",
            data=buffer.getvalue(),
            file_name=f"servicos_{cliente_id_input}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        st.divider()
        st.markdown("### Tickets")
        
        tickets_dados = load_tickets_data(cliente_id_input)
        if tickets_dados is not None:
            df_tickets = pd.DataFrame(tickets_dados)
            if not df_tickets.empty:
                selected_rows = event.selection.rows
                if selected_rows:
                    selected_service = df.iloc[selected_rows[0]]["SERVIÇO"]
                    df_tickets_filtered = df_tickets[df_tickets["SERVIÇO"] == selected_service]
                    st.info(f"Mostrando tickets filtrados para o SERVIÇO selecionado: {selected_service}")
                else:
                    df_tickets_filtered = df_tickets
                    st.info("Mostrando todos os tickets do cliente (clique em um serviço acima para filtrar).")

                st.dataframe(
                    df_tickets_filtered, 
                    use_container_width=True,
                    column_config={    
                        "SERVIÇO": st.column_config.NumberColumn("SERVIÇO", format="%d"), 
                        "Nº PLANO": st.column_config.NumberColumn("Nº PLANO", format="%d"),
                        "TICKET": st.column_config.NumberColumn("TICKET", format="%d"),
                        "PROTOCOLO": st.column_config.NumberColumn("PROTOCOLO", format="%d")
                    }
                )
                
                buffer_tickets = io.BytesIO()
                df_tickets_filtered.to_excel(buffer_tickets, index=False)
                
                st.download_button(
                    label="📥 Exportar Tickets para Excel",
                    data=buffer_tickets.getvalue(),
                    file_name=f"tickets_{cliente_id_input}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("Nenhum ticket encontrado detalhadamente para este cliente.")
