from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    JSON,
    ForeignKey,
    DateTime,
    func,
    Numeric,
    Enum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SearchQuery(Base):
    __tablename__ = "search_queries"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    region = Column(Enum('BR', 'US', 'EU', name='region_enum', create_type=False), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    filters = relationship("Filter", back_populates="search_query")
    products = relationship("Product", back_populates="search_query")


class Filter(Base):
    __tablename__ = "filters"

    id = Column(Integer, primary_key=True, index=True)
    search_query_id = Column(Integer, ForeignKey("search_queries.id"), nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    search_query = relationship("SearchQuery", back_populates="filters")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    google_product_id = Column(String(255), unique=True, nullable=False, index=True)
    search_query_id = Column(Integer, ForeignKey("search_queries.id"), nullable=False)
    region = Column(Enum('BR', 'US', 'EU', name='region_enum', create_type=False), nullable=False)
    title = Column(String(512), nullable=False)
    brand = Column(String(255), index=True)
    price = Column(Numeric(10, 2))
    thumbnail_url = Column(String)
    store_name = Column(String(255))
    store_link = Column(String, nullable=False)
    rating = Column(Numeric(3, 2))
    reviews = Column(Integer)
    variants = Column(JSON)
    other_details = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    search_query = relationship("SearchQuery", back_populates="products")