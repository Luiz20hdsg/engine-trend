import os
import requests
import json
from typing import Optional
from sqlalchemy.orm import Session
from app.core.config import settings
from app.database import models
from app.crud import crud_stores, crud_brands, crud_products, crud_trends

# Mapeamento de regiões para parâmetros da API do Serper
REGION_PARAMS = {
    "BR": {"gl": "br", "hl": "pt", "google_domain": "google.com.br"},
    "US": {"gl": "us", "hl": "en", "google_domain": "google.com"},
    "EU": {"gl": "de", "hl": "de", "google_domain": "google.de"},
}

# Lista inicial de marcas para procurar nos títulos dos produtos.
# O ideal é que isso venha do banco de dados no futuro.
KNOWN_BRANDS = [
    "Nike", "Adidas", "Shein", "Renner", "C&A", "Zara", "Hering", "Moleca", 
    "Vizzano", "Dakota", "Colcci", "Farm", "Schutz", "Arezzo", "Melissa"
]

class ProductEnricher:
    """
    Busca produtos para uma tendência, os enriquece com marca/categoria e os salva no banco.
    """
    def __init__(self, db_session: Session):
        self.db = db_session
        self.serper_api_key = settings.SERPER_API_KEY

    def _find_products(self, query: str, region: str, limit: int = 10) -> list:
        # ... (código do método _find_products permanece o mesmo)
        if not self.serper_api_key:
            print("Erro: Chave de API do Serper não configurada.")
            return []

        if region.upper() not in REGION_PARAMS:
            print(f"Erro: Região '{region}' não suportada.")
            return []

        url = "https://google.serper.dev/shopping"
        params = REGION_PARAMS[region.upper()]
        payload = json.dumps({"q": query, "num": limit, **params})
        headers = {'X-API-KEY': self.serper_api_key, 'Content-Type': 'application/json'}

        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            return response.json().get("shopping", [])
        except requests.exceptions.RequestException as e:
            print(f"Erro ao chamar a API do Serper: {e}")
            return []

    def _extract_brand_id(self, product_title: str) -> Optional[int]:
        """Extrai uma marca conhecida do título de um produto."""
        for brand_name in KNOWN_BRANDS:
            if brand_name.lower() in product_title.lower():
                brand = crud_brands.get_or_create_brand(self.db, brand_name=brand_name)
                return brand.id
        return None

    def enrich(self, trend: models.Trend):
        """Enriquece uma tendência com produtos, incluindo loja, marca e categoria."""
        print(f"\n--- Enriquecendo a tendência: '{trend.name}' para a região {trend.region} ---")
        products = self._find_products(query=trend.name, region=trend.region)

        if not products:
            print("Nenhum produto encontrado.")
            return

        # Busca a categoria da tendência para associar aos produtos
        category = self.db.query(models.Category).filter(models.Category.slug == trend.category).first()
        category_id = category.id if category else None
        if not category_id:
            print(f"Alerta: Categoria '{trend.category}' não encontrada no banco. Os produtos não serão categorizados.")

        print(f"{len(products)} produtos encontrados. Salvando no banco...")
        saved_count = 0
        for product_data in products:
            store_name = product_data.get('source')
            product_title = product_data.get('title', '')
            if not store_name or not product_title:
                continue

            # 1. Garante que a loja exista
            store = crud_stores.get_or_create_store(self.db, store_name=store_name)

            # 2. Extrai a marca do título do produto
            brand_id = self._extract_brand_id(product_title)

            # 3. Cria o produto e associações
            crud_products.create_product(
                self.db,
                product_data=product_data,
                store_id=store.id,
                trend_id=trend.id,
                brand_id=brand_id,
                category_id=category_id
            )
            saved_count += 1
        
        print(f"{saved_count} produtos salvos e associados à tendência '{trend.name}'.")

# --- Bloco de Teste ---
if __name__ == '__main__':
    from app.database.session import SessionLocal

    print("--- Iniciando teste de integração do ProductEnricher ---")
    db_session = SessionLocal()
    try:
        # 1. Pega a última tendência salva no banco de dados
        latest_trend = db_session.query(models.Trend).order_by(models.Trend.id.desc()).first()

        if not latest_trend:
            print("Nenhuma tendência encontrada no banco para testar. Execute o trend_processor primeiro.")
        else:
            # 2. Enriquece a tendência com produtos
            enricher = ProductEnricher(db_session)
            enricher.enrich(trend=latest_trend)
            print("\n--- Teste de enriquecimento concluído ---")

    finally:
        db_session.close()