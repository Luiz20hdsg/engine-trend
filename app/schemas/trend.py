from pydantic import BaseModel
from typing import Optional, List

# Schema base para Categoria, usado para leitura
class CategoryBase(BaseModel):
    id: int
    name: str
    slug: str
    parent_id: Optional[int] = None

# Este é o schema que será usado ao retornar dados da API.
# orm_mode = True diz ao Pydantic para ler os dados de um objeto ORM (nosso modelo SQLAlchemy)
class Category(CategoryBase):
    class Config:
        from_attributes = True

# Schema para criação (se necessário no futuro)
class CategoryCreate(BaseModel):
    name: str
    slug: str
    parent_id: Optional[int] = None


# --- Schemas para Trend --- #

class TrendBase(BaseModel):
    name: str
    source: str
    category: str
    region: str
    score: int = 0
    description: Optional[str] = None

class TrendCreate(TrendBase):
    pass

class Trend(TrendBase):
    id: int
    inspiration_images: Optional[list] = []

    class Config:
        from_attributes = True
