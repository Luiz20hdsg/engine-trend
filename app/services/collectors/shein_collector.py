import os
import re
from bs4 import BeautifulSoup
from .base_collector import BaseCollector

class SheinCollector(BaseCollector):
    """
    Coleta dados de tendências da Shein a partir de arquivos locais.
    """
    def __init__(self):
        self.html_files = {
            'BR': 'shein_br.html',
            'EU': 'shein_eu.html',
            'US': 'shein_us.html'
        }
        self.base_path = "/Users/mymac/trend-engine/app/services/collectors/manual_html"

    def _clean_description(self, description: str) -> str:
        """
        Remove marcas e palavras-chave de marketing das descrições dos produtos.
        """
        # Lista de marcas e termos a serem removidos
        brands_to_remove = [
            'SHEIN', 'DAZY', 'EMERY ROSE', 'ROMWE', 'MOTF', 'BIZCHIC', 'MUSERA',
            'Coolane', 'Anewsta', 'Firerie', 'Calvaya', 'Livesso', 'Poéselle',
            'Ontre', 'Maija', 'Attitoon', 'Mulvari', 'Sollinarry', 'Flirla',
            'RosyDaze', 'COSMINA', 'Elenzga', 'Breezaya', 'INAWLY', 'Aveloria',
            'Sweetra', 'Siren Gaze', 'LUNE', 'BAE', 'EZwear', 'Clasi',
            'PETITE', 'ICON', 'MOD', 'Frenchy', 'Unity', 'Swim', 'Essnce'
        ]
        # Constrói um padrão regex para encontrar qualquer uma dessas marcas como palavras inteiras
        # e de forma case-insensitive, incluindo colaborações como "SHEIN x Artist"
        pattern = r'\b(' + '|'.join(brands_to_remove) + r')(\s*x\s*[A-Za-z]+)?\b'
        
        # Remove as marcas da descrição
        cleaned_desc = re.sub(pattern, '', description, flags=re.IGNORECASE)
        
        # Remove hífens no início e espaços em branco extras
        cleaned_desc = cleaned_desc.lstrip(' -').strip()
        
        # Remove múltiplos espaços por um único espaço
        cleaned_desc = re.sub(r'\s+', ' ', cleaned_desc)
        
        return cleaned_desc

    def collect(self, region: str = 'BR'):
        """
        Busca as tendências da Shein para uma determinada região a partir de um arquivo local.

        :param region: O código da região (BR, EU, US).
        :return: Uma lista de nomes de tendências limpos.
        """
        region_upper = region.upper()
        file_name = self.html_files.get(region_upper)
        
        if not file_name:
            print(f"Região '{region}' não suportada para Shein.")
            return []

        file_path = os.path.join(self.base_path, file_name)
        print(f"Iniciando coleta de Shein para a região: {region_upper} a partir do arquivo: {file_path}")

        if region_upper == 'US':
            print("Coleta para os EUA não é suportada pois o conteúdo é dinâmico e não pode ser lido do arquivo HTML estático.")
            return []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            trends = [self._clean_description(line) for line in lines if line.strip()]

            print(f"Encontradas {len(trends)} tendências na Shein para a região {region_upper}.")
            return trends

        except FileNotFoundError:
            print(f"Arquivo não encontrado para a região {region_upper}: {file_path}")
            return []
        except Exception as e:
            print(f"Ocorreu um erro ao processar o arquivo da Shein para a região {region_upper}: {e}")
            return []

if __name__ == '__main__':
    collector = SheinCollector()

    print("\n--- Processando Região BR ---")
    br_trends = collector.collect(region='BR')
    print("5 primeiras tendências limpas para o Brasil:")
    print(br_trends[:5])

    print("\n--- Processando Região EU ---")
    eu_trends = collector.collect(region='EU')
    print("5 primeiras tendências limpas para a Europa:")
    print(eu_trends[:5])

    print("\n--- Processando Região US ---")
    us_trends = collector.collect(region='US')
    print("Tendências para os EUA:")
    print(us_trends)