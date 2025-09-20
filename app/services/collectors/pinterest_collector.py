from .base_collector import BaseCollector

class PinterestCollector(BaseCollector):
    """
    Coleta dados de tendências do Pinterest usando a API oficial.
    (A ser implementado no futuro)
    """
    def __init__(self, api_key, api_secret):
        # A inicialização com as credenciais da API será feita aqui
        pass

    def collect(self, region: str):
        print("INFO: O coletor do Pinterest ainda não foi implementado.")
        return []
