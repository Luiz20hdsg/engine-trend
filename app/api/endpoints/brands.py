from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import crud_brands
from app.schemas import brand

router = APIRouter()

@router.get("/brands", response_model=List[brand.Brand])
def read_brands(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Recupera uma lista de marcas.
    """
    brands = crud_brands.get_brands(db, skip=skip, limit=limit)
    return brands
