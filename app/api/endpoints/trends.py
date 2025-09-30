from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_trends as crud_catalog
from app.schemas import trend as catalog_schema
from app.database.models import RegionEnum

router = APIRouter()

@router.get("/filters", response_model=List[catalog_schema.Filter])
def read_filters(
    category: str,
    region: RegionEnum,
    db: Session = Depends(deps.get_db),
):
    """
    Recupera uma lista de filtros para uma determinada categoria e região.
    """
    # This logic is simplified. We might need a more robust way to link
    # a category to a search_query. For now, we assume a direct match.
    search_query = crud_catalog.get_search_query_by_name_and_region(db, query=category, region=region.value)
    if not search_query:
        return []
    return crud_catalog.get_filters_by_query_id(db, search_query_id=search_query.id)


@router.get("/products", response_model=List[catalog_schema.Product])
def read_products(
    region: RegionEnum,
    db: Session = Depends(deps.get_db),
    category: str = None,
    brand: str = None,
    price_max: float = None,
    skip: int = 0,
    limit: int = 100,
):
    """
    Recupera uma lista de produtos do catálogo, com filtros.
    """
    products = crud_catalog.get_products_by_region(
        db,
        region=region.value,
        category=category,
        brand=brand,
        price_max=price_max,
        skip=skip,
        limit=limit
    )
    return products