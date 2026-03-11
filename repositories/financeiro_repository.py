from db_connections import get_atrix_connection


class FinanceiroRepository:

    @staticmethod
    def get_resumo(cliente_id):

        query = open("queries/financeiro_cliente.sql").read()

        conn = get_atrix_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(query, (cliente_id,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def get_descontos_servico(servico_id):

        query = open("queries/descontos_servico.sql").read()

        conn = get_atrix_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(query, (servico_id,))
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return result