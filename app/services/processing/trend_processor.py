from sqlalchemy.orm import Session
from app.crud import crud_trends
from app.schemas import trend as trend_schema
from .category_mapper import get_mapped_category_slug

class TrendProcessor:
    """
    Processa dados brutos de tendências, salva no banco e despacha tarefas de enriquecimento.
    """
    def __init__(self, db_session: Session):
        self.db = db_session

    def process(self, trend_data: list[dict]):
        """
        Processa uma lista de dados de tendências. 
        FORÇARÁ O ENRIQUECIMENTO de todas as tendências encontradas.
        """
        if not trend_data or not isinstance(trend_data, list):
            print("Dados de tendência inválidos ou vazios.")
            return

        print(f"Processando {len(trend_data)} tendências com enriquecimento forçado...")
        trends_criadas = 0
        for item in trend_data:
            trend_name = item.get('name')
            region = item.get('region')
            source = item.get('source')
            source_category = item.get('category')

            # Mapeia a categoria da fonte para o slug do sistema
            mapped_slug = get_mapped_category_slug(source_category)

            if not all([trend_name, region, source, mapped_slug]):
                if not mapped_slug:
                    print(f"Alerta: Categoria da fonte '{source_category}' não pôde ser mapeada. Ignorando tendência '{trend_name}'.")
                else:
                    print(f"Item de tendência inválido ignorado: {item}")
                continue

            score = item.get('score', 0)

            # Tenta buscar a tendência no banco
            db_trend = crud_trends.get_trend_by_name_and_region(
                self.db, name=trend_name, region=region
            )

            # Se não existir, cria uma nova
            if not db_trend:
                trend_in = trend_schema.TrendCreate(
                    name=trend_name,
                    score=score,
                    region=region,
                    source=source,
                    category=mapped_slug, # Usa o slug mapeado
                    description=f"Tendência coletada da fonte: {source}."
                )
                db_trend = crud_trends.create_trend(self.db, trend=trend_in)
                trends_criadas += 1
            
            # Garante que temos um objeto de tendência (novo ou existente)
            # e despacha a tarefa de enriquecimento para ele.
            if db_trend:
                from app.services.tasks import enrich_trend
                print(f"Disparando enriquecimento para Trend ID: {db_trend.id} ({db_trend.name})")
                enrich_trend.delay(db_trend.id)
        
        if trends_criadas > 0:
            print(f"{trends_criadas} novas tendências foram salvas.")
        else:
            print("Nenhuma tendência nova foi criada (mas o enriquecimento foi disparado para as existentes).")