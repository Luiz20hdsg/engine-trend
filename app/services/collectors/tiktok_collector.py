import os
from .base_collector import BaseCollector

class TikTokCollector(BaseCollector):
    """
    Coleta hashtags de tendências do TikTok a partir de arquivos de texto locais.
    """
    def __init__(self):
        self.base_path = "/Users/mymac/trend-engine/app/services/collectors/manual_html/tiktok"
        self.category_files = {
            'BEAUTY_PERSONAL_CARE': 'br_beauty_personal_care.txt',
            'APPAREL_ACCESSORIES': 'br_apparel_accessories.txt'
        }

    def collect(self, category: str):
        """
        Busca as hashtags de uma determinada categoria a partir de um arquivo local.

        :param category: A categoria de interesse (BEAUTY_PERSONAL_CARE, APPAREL_ACCESSORIES).
        :return: Uma lista de hashtags.
        """
        category_upper = category.upper()
        file_name = self.category_files.get(category_upper)

        if not file_name:
            print(f"Categoria '{category}' não suportada para TikTok.")
            return []

        file_path = os.path.join(self.base_path, file_name)
        print(f"Iniciando coleta de TikTok para a categoria: {category_upper} a partir do arquivo: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                trends = [line.strip() for line in f.readlines() if line.strip()]

            print(f"Encontradas {len(trends)} tendências no TikTok para a categoria {category_upper}.")
            return trends

        except FileNotFoundError:
            print(f"Arquivo de hashtags não encontrado para a categoria {category_upper}: {file_path}")
            return []
        except Exception as e:
            print(f"Ocorreu um erro ao processar o arquivo do TikTok para a categoria {category_upper}: {e}")
            return []

if __name__ == '__main__':
    collector = TikTokCollector()

    print("\n--- Processando Categoria Beauty & Personal Care ---")
    beauty_trends = collector.collect(category='BEAUTY_PERSONAL_CARE')
    print("5 primeiras tendências de Beleza e Cuidados Pessoais:")
    print(beauty_trends[:5])

    print("\n--- Processando Categoria Apparel & Accessories ---")
    apparel_trends = collector.collect(category='APPAREL_ACCESSORIES')
    print("5 primeiras tendências de Vestuário e Acessórios:")
    print(apparel_trends[:5])