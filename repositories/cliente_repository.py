from queries.db_connections import get_atrix_connection


class ClienteRepository:

    @staticmethod
    def get_by_cnpj(cnpj):

        query = open("queries/cliente_por_cnpj.sql").read()

        conn = get_atrix_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(query, (cnpj,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result