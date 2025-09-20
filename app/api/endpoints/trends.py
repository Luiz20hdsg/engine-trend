from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_trends
from app.schemas import trend as trend_schemas

# Cria um novo roteador
router = APIRouter()

@router.get("/categories", response_model=List[trend_schemas.Category])
def read_categories(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Recupera uma lista de categorias.
    Este será usado pelo app para exibir os filtros.
    """
    categories = crud_trends.get_categories(db, skip=skip, limit=limit)
    return categories


@router.get("/trends", response_model=List[trend_schemas.Trend])
def read_trends(
    db: Session = Depends(deps.get_db),
    region: str = None,
    category: str = None,
    skip: int = 0,
    limit: int = 100,
):
    """
    Recupera uma lista de tendências, com filtros opcionais por região e categoria.
    """
    trends = crud_trends.get_trends(db, region=region, category=category, skip=skip, limit=limit)
    return trends
