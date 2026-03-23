import requests
from queries.db_connections import get_atrix_connection


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

    @staticmethod
    def get_faturas_servico(servico_id):
        try:
            url = f"https://apib2b.mobtelecom.com.br/api/v1/managerService/invoices?relid={servico_id}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    return data
                # Caso a resposta seja um dicionário envolvendo a lista, lida-se com as chaves apropriadas se houver, mas assumiremos lista.
            return []
        except Exception as e:
            print(f"Erro ao buscar faturas na API: {e}")
            return []