from db_connections import get_atrix_connection


class ServicoRepository:

    @staticmethod
    def listar_por_cliente(cliente_id):

        query = open("queries/servicos_cliente.sql").read()

        conn = get_atrix_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(query, (cliente_id,))
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return result