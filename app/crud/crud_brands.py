from sqlalchemy.orm import Session
from app.database import models

def get_brands(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Brand).offset(skip).limit(limit).all()

def get_or_create_brand(db: Session, brand_name: str) -> models.Brand:
    """Busca uma marca pelo nome, se não existir, cria uma nova."""
    brand = db.query(models.Brand).filter(models.Brand.name == brand_name).first()
    if not brand:
        brand = models.Brand(name=brand_name)
        db.add(brand)
        db.commit()
        db.refresh(brand)
    return brand
