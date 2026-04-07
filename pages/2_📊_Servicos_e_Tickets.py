import streamlit as st
import pandas as pd
import io
from services.servicos_service import ServicoService
from services.tickets_service import TicketService

st.set_page_config(page_title="Serviços e Tickets", layout="wide", page_icon="📊")

st.markdown("## 📊 Serviços e Tickets por Cliente")
st.divider()

# Campo de texto para buscar outro ID, com o 6971 como padrão default
cliente_id_input = st.text_input("Buscar por ID do Cliente", value="6971")

if not cliente_id_input:
    st.info("Informe um ID de cliente para analisar.")
    st.stop()

# Spinner nativo para indicar carregamento
with st.spinner("Carregando dados..."):
    df = ServicoService.get_servicos_tickets_df(cliente_id_input)

if df is not None:
    if df.empty:
        st.warning(f"Nenhum serviço/ticket encontrado para o cliente de ID: {cliente_id_input}.")
    else:
        st.success(f"Busca finalizada! {len(df)} registro(s) encontrado(s).")
        
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
        
        df_tickets = TicketService.get_tickets_por_cliente_df(cliente_id_input)
        if df_tickets is not None:
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
