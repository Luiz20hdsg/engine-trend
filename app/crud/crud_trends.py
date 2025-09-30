from sqlalchemy.orm import Session
from app.database import models
from app.schemas import trend as catalog_schema # I'm using 'trend' as it's the real filename

# CRUD for SearchQuery
def get_search_query(db: Session, query_id: int):
    return db.query(models.SearchQuery).filter(models.SearchQuery.id == query_id).first()

def get_search_query_by_name(db: Session, query: str):
    return db.query(models.SearchQuery).filter(models.SearchQuery.query == query).first()

def get_active_search_queries(db: Session):
    return db.query(models.SearchQuery).filter(models.SearchQuery.is_active == True).all()

def get_active_search_queries_by_region(db: Session, region: str):
    return db.query(models.SearchQuery).filter(models.SearchQuery.is_active == True, models.SearchQuery.region == region.upper()).all()

def get_search_query_by_name_and_region(db: Session, query: str, region: str):
    return db.query(models.SearchQuery).filter(models.SearchQuery.query == query, models.SearchQuery.region == region.upper()).first()

# CRUD for Filter
def get_or_create_filter(db: Session, search_query_id: int, name: str, type: str):
    db_filter = db.query(models.Filter).filter(models.Filter.search_query_id == search_query_id, models.Filter.name == name).first()
    if not db_filter:
        db_filter = models.Filter(search_query_id=search_query_id, name=name, type=type)
        db.add(db_filter)
        db.commit()
        db.refresh(db_filter)
    return db_filter

def get_filters_by_query_id(db: Session, search_query_id: int):
    return db.query(models.Filter).filter(models.Filter.search_query_id == search_query_id).all()

# CRUD for Product
def create_or_update_product(db: Session, product: catalog_schema.ProductCreate):
    """
    Creates a new product or updates it if it already exists based on google_product_id.
    """
    db_product = db.query(models.Product).filter(models.Product.google_product_id == product.google_product_id).first()

    if db_product:
        # Update existing product
        update_data = product.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
    else:
        # Create new product
        db_product = models.Product(**product.model_dump())
        db.add(db_product)
    
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products_by_region(db: Session, region: str, skip: int = 0, limit: int = 100, category: str = None, brand: str = None, price_max: float = None):
    query = db.query(models.Product).filter(models.Product.region == region.upper())
    if category:
        # This requires a join with search_queries
        query = query.join(models.SearchQuery).filter(models.SearchQuery.category == category)
    if brand:
        query = query.filter(models.Product.brand.ilike(f"%{brand}%"))
    if price_max:
        query = query.filter(models.Product.price <= price_max)
        
    return query.offset(skip).limit(limit).all()