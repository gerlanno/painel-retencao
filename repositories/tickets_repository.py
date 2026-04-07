from queries.db_connections import get_atrix_connection


class TicketRepository:

    @staticmethod
    def listar_por_servico(servico_id):

        query = open("queries/tickets_servico.sql").read()

        conn = get_atrix_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(query, (servico_id,))
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def listar_por_cliente(cliente_id):
        query = open("queries/tickets_por_cliente.sql", encoding='utf-8').read()

        conn = get_atrix_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(query, (cliente_id,))
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return result