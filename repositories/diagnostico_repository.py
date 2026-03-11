from db_connections import get_atrix_connection


class DiagnosticoRepository:

    @staticmethod
    def get_diagnostico(servico_id):

        query_geral = open("queries/diagnostico.sql").read()
        query_motivos = open("queries/resumo_motivos.sql").read()
        query_sla = open("queries/resumo_sla.sql").read()
        query_encerramento = open("queries/resumo_encerramento.sql").read()

        query_mensal = open("queries/resumo_mensal_tickets.sql").read()

        conn = get_atrix_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(query_geral, (servico_id,))
        geral = cursor.fetchone()
        
        if geral:
            cursor.execute(query_motivos, (servico_id,))
            geral["motivos_90d"] = cursor.fetchall()
            
            cursor.execute(query_sla, (servico_id,))
            geral["sla_90d"] = cursor.fetchone()
            
            cursor.execute(query_encerramento, (servico_id,))
            geral["encerrados_90d"] = cursor.fetchall()

            cursor.execute(query_mensal, (servico_id,))
            geral["evolucao_12m"] = cursor.fetchall()

        cursor.close()
        conn.close()

        return geral