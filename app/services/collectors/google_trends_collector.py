from pytrends.request import TrendReq
import pandas as pd
from .base_collector import BaseCollector

class GoogleTrendsCollector(BaseCollector):
    """
    Coleta dados de tendências de moda do Google Trends.
    """
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)
        # Palavra-chave de categoria para Moda e Estilo no Google Trends
        # O ID pode variar, mas 'fashion' costuma ser mapeado para a categoria correta.
        self.fashion_category_id = 14

    def collect(self, region: str = 'US'):
        """
        Busca as "rising queries" (buscas em ascensão) relacionadas a moda
        para uma determinada região.

        :param region: O código do país de duas letras (ex: 'US', 'BR').
        :return: Um dicionário com os termos em ascensão ou uma mensagem de erro.
        """
        print(f"Iniciando coleta de Google Trends para a região: {region.upper()}")
        try:
            # Busca as "rising queries" para a categoria de moda
            self.pytrends.build_payload(
                kw_list=['fashion'], # Palavra-chave genérica para filtrar
                cat=self.fashion_category_id,
                timeframe='today 1-m', # Tendências do último mês
                geo=region.upper()
            )
            
            related_queries = self.pytrends.related_queries()
            rising_queries = related_queries.get('fashion', {}).get('rising')

            if rising_queries is not None and not rising_queries.empty:
                print(f"Encontradas {len(rising_queries)} tendências em ascensão.")
                # Retorna os dados como uma lista de dicionários
                return rising_queries.to_dict('records')
            else:
                print("Nenhuma tendência em ascensão encontrada para esta região/categoria.")
                return {"message": "No rising trends found."}

        except Exception as e:
            print(f"Ocorreu um erro ao coletar dados do Google Trends: {e}")
            return {"error": str(e)}

# Exemplo de como usar (para teste)
if __name__ == '__main__':
    collector = GoogleTrendsCollector()
    # Testando para o Brasil
    br_trends = collector.collect(region='BR')
    print("\n--- Tendências Brasil ---")
    print(br_trends)

    # Testando para os EUA
    us_trends = collector.collect(region='US')
    print("\n--- Tendências EUA ---")
    print(us_trends)
