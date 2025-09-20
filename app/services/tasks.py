from app.core.celery_app import celery_app
from app.database.session import SessionLocal
from app.services.processing.trend_processor import TrendProcessor
from app.services.processing.product_enricher import ProductEnricher
from app.crud import crud_trends
from app.schemas import trend as trend_schema

@celery_app.task(acks_late=True)
def enrich_trend(trend_id: int):
    """
    Tarefa Celery para enriquecer uma única tendência com produtos.
    """
    print(f"Iniciando tarefa de enriquecimento para a tendência ID: {trend_id}")
    db = SessionLocal()
    try:
        trend = crud_trends.get_trend_by_id(db, trend_id=trend_id)
        if trend:
            enricher = ProductEnricher(db)
            enricher.enrich(trend)
            print(f"Tarefa de enriquecimento para a tendência ID: {trend_id} concluída.")
        else:
            print(f"Tendência ID: {trend_id} não encontrada para enriquecimento.")
    finally:
        db.close()

from app.services.collectors.shein_collector import SheinCollector
from app.services.collectors.tiktok_collector import TikTokCollector
from app.services.collectors.google_trends_collector import GoogleTrendsCollector

@celery_app.task(acks_late=True)
def collect_and_process_trends(region: str):
    """
    Tarefa Celery para coletar dados de todas as fontes e processá-los.
    """
    print(f"Iniciando tarefa de coleta e processamento para a região: {region}")
    
    all_trends_data = []
    
    # Configuração das coletas. Cada dicionário especifica um coletor e seus parâmetros.
    collection_configs = [
        # Coleta do Google Trends
        {"collector": GoogleTrendsCollector(), "params": {"region": region}, "source": "GoogleTrends", "category": "general"},
        # Coleta da Shein para BR
        {"collector": SheinCollector(), "params": {"region": "BR"}, "source": "Shein", "category": "ready-to-wear"},
        # Coleta da Shein para EU
        {"collector": SheinCollector(), "params": {"region": "EU"}, "source": "Shein", "category": "ready-to-wear"},
        # Coleta do TikTok para BR - Vestuário
        {"collector": TikTokCollector(), "params": {"category": "APPAREL_ACCESSORIES"}, "source": "TikTok", "category": "ready-to-wear"},
        # Coleta do TikTok para BR - Beleza
        {"collector": TikTokCollector(), "params": {"category": "BEAUTY_PERSONAL_CARE"}, "source": "TikTok", "category": "beleza"},
    ]

    for config in collection_configs:
        collector = config["collector"]
        params = config["params"]
        source = config["source"]
        category = config["category"]
        
        current_region = params.get("region", "BR") # Default to BR for TikTok

        print(f"-- Verificando coletor: {source} para a região: {current_region.upper()}. Tarefa atual para a região: {region.upper()} --")

        # Filtra a execução para a região especificada na tarefa
        if region.upper() != current_region.upper():
            print(f"-- IGNORANDO COLETOR: {source} pois a região não corresponde.")
            continue

        print(f"Executando coletor: {collector.__class__.__name__} com params: {params}")
        try:
            collected_data = collector.collect(**params)
            
            if not collected_data:
                print(f"Coletor {collector.__class__.__name__} não retornou dados para {params}.")
                continue

            # Lida com os diferentes formatos de retorno dos coletores
            if isinstance(collected_data, list) and collected_data:
                if isinstance(collected_data[0], str): # Lista de strings (Shein, TikTok)
                    for name in collected_data:
                        all_trends_data.append({
                            "name": name,
                            "region": current_region.upper(),
                            "source": source,
                            "category": category,
                            "score": 0
                        })
                elif isinstance(collected_data[0], dict): # Lista de dicts (Google Trends)
                    for item in collected_data:
                        all_trends_data.append({
                            "name": item.get("query"),
                            "region": current_region.upper(),
                            "source": source,
                            "category": category,
                            "score": item.get("value", 0)
                        })

        except Exception as e:
            print(f"Erro ao executar o coletor {collector.__class__.__name__} com params {params}: {e}")

    if not all_trends_data:
        print(f"Nenhum dado foi coletado para a região: {region}. A tarefa será encerrada.")
        return

    # Processar os dados combinados
    db = SessionLocal()
    try:
        processor = TrendProcessor(db)
        processor.process(trend_data=all_trends_data)
        print(f"Tarefa de coleta e processamento para a região: {region} concluída.")
    finally:
        db.close()

@celery_app.task
def test_enrichment():
    """
    Tarefa de teste para diagnosticar o problema de enriquecimento.
    """
    db = SessionLocal()
    try:
        print("--- INICIANDO TAREFA DE TESTE DE ENRIQUECIMENTO ---")
        # 1. Pega ou cria uma tendência de teste
        trend_name = "Teste de Categoria"
        region = "BR"
        category_slug = "beleza" # Usando um slug que sabemos que existe
        
        trend = crud_trends.get_trend_by_name_and_region(db, name=trend_name, region=region)
        if not trend:
            print(f"Criando tendência de teste: {trend_name}")
            trend_in = trend_schema.TrendCreate(
                name=trend_name,
                region=region,
                source="Test",
                category=category_slug,
                score=100
            )
            trend = crud_trends.create_trend(db, trend=trend_in)
        
        # 2. Chama o enriquecimento para essa tendência
        print(f"Disparando enriquecimento para a tendência de teste ID: {trend.id}")
        enricher = ProductEnricher(db)
        enricher.enrich(trend)
        print("--- TAREFA DE TESTE CONCLUÍDA ---")
        
    finally:
        db.close()