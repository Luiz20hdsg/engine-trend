from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import crud_stores
from app.schemas import store

router = APIRouter()

@router.get("/stores", response_model=List[store.Store])
def read_stores(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Recupera uma lista de lojas.
    """
    stores = crud_stores.get_stores(db, skip=skip, limit=limit)
    return stores
