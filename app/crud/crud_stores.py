from sqlalchemy.orm import Session
from app.database import models

def get_stores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Store).offset(skip).limit(limit).all()

def get_or_create_store(db: Session, store_name: str) -> models.Store:
    """Busca uma loja pelo nome, se não existir, cria uma nova."""
    store = db.query(models.Store).filter(models.Store.name == store_name).first()
    if not store:
        store = models.Store(name=store_name)
        db.add(store)
        db.commit()
        db.refresh(store)
    return store
