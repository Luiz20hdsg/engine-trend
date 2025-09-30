from pydantic import BaseModel
from typing import List, Optional

# Schemas for Product
class ProductBase(BaseModel):
    google_product_id: str
    title: str
    brand: Optional[str] = None
    price: Optional[float] = None
    thumbnail_url: Optional[str] = None
    store_name: Optional[str] = None
    store_link: str
    rating: Optional[float] = None
    reviews: Optional[int] = None
    variants: Optional[dict] = None
    other_details: Optional[dict] = None

class ProductCreate(ProductBase):
    search_query_id: int

class Product(ProductBase):
    id: int
    search_query_id: int

    class Config:
        orm_mode = True

# Schemas for Filter
class FilterBase(BaseModel):
    name: str
    type: Optional[str] = None

class FilterCreate(FilterBase):
    pass

class Filter(FilterBase):
    id: int
    search_query_id: int

    class Config:
        orm_mode = True

# Schemas for SearchQuery
class SearchQueryBase(BaseModel):
    query: str
    category: str
    is_active: bool = True

class SearchQueryCreate(SearchQueryBase):
    pass

class SearchQuery(SearchQueryBase):
    id: int
    filters: List[Filter] = []
    products: List[Product] = []

    class Config:
        orm_mode = True