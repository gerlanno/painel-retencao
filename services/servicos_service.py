import pandas as pd
from repositories.servicos_cliente import ServicoRepository

class ServicoService:
    @staticmethod
    def get_servicos_tickets_df(cliente_id):
        """Busca e retorna serviços formatados em um DataFrame."""
        resultados = ServicoRepository.listar_com_tickets_por_cliente(cliente_id)
        
        if not resultados:
            return None
            
        df = pd.DataFrame(resultados)
        return df
