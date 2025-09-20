from typing import Union
from sqlalchemy.orm import Session
from app.database import models
from app.schemas import trend as trend_schema

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    """
    Busca categorias no banco de dados.
    """
    return db.query(models.Category).offset(skip).limit(limit).all()

def get_trend_by_id(db: Session, trend_id: int) -> Union[models.Trend, None]:
    """
    Busca uma tendência específica pelo seu ID.
    """
    return db.query(models.Trend).filter(models.Trend.id == trend_id).first()

def get_trends(db: Session, region: str = None, category: str = None, skip: int = 0, limit: int = 100):
    """
    Busca tendências no banco de dados, com filtros opcionais por região e categoria.
    """
    query = db.query(models.Trend)
    if region:
        query = query.filter(models.Trend.region == region.upper())
    if category:
        query = query.filter(models.Trend.category == category)
    return query.offset(skip).limit(limit).all()

def get_trend_by_name_and_region(db: Session, name: str, region: str) -> Union[models.Trend, None]:
    """
    Busca uma tendência específica pelo nome e região.
    """
    return db.query(models.Trend).filter(models.Trend.name == name, models.Trend.region == region.upper()).first()

def create_trend(db: Session, trend: trend_schema.TrendCreate) -> models.Trend:
    """
    Cria uma nova tendência no banco de dados.
    """
    # Usa model_dump() que é o método correto para Pydantic v2
    db_trend = models.Trend(**trend.model_dump())
    db.add(db_trend)
    db.commit()
    db.refresh(db_trend)
    return db_trend
