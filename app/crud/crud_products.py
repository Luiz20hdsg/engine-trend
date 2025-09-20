from sqlalchemy.orm import Session
from app.database import models

def create_product(
    db: Session, 
    product_data: dict, 
    store_id: int, 
    trend_id: int, 
    brand_id: int = None, 
    category_id: int = None
) -> models.Product:
    """
    Cria um novo produto e o associa a uma tendência, loja, e opcionalmente a uma marca e categoria.
    """
    # 1. Cria a instância do produto
    db_product = models.Product(
        title=product_data.get('title'),
        link=product_data.get('link'),
        price=product_data.get('price'),
        thumbnail=product_data.get('imageUrl'),
        store_id=store_id,
        brand_id=brand_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    # 2. Associa o produto à tendência na tabela 'trend_products'
    trend = db.query(models.Trend).filter(models.Trend.id == trend_id).first()
    if trend:
        trend.products.append(db_product)
        db.commit()

    # 3. Associa o produto à categoria na tabela 'product_categories'
    if category_id:
        category = db.query(models.Category).filter(models.Category.id == category_id).first()
        if category:
            db_product.categories.append(category)
            db.commit()
            
    return db_product
