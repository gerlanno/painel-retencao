import pandas as pd
from repositories.tickets_repository import TicketRepository

class TicketService:
    @staticmethod
    def get_tickets_por_cliente_df(cliente_id):
        """Busca e retorna tickets do cliente formatados em um DataFrame."""
        resultados = TicketRepository.listar_por_cliente(cliente_id)
        
        if not resultados:
            return None
            
        df = pd.DataFrame(resultados)
        return df
