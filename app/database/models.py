from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Table,
    JSON
)
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()

# Tabela de associação Muitos-para-Muitos entre Trends e Products
trend_products = Table(
    'trend_products',
    Base.metadata,
    Column('trend_id', Integer, ForeignKey('trends.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True)
)

# Tabela de associação Muitos-para-Muitos entre Products e Categories
product_categories = Table(
    'product_categories',
    Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    parent_id = Column(Integer, ForeignKey('categories.id'))

    parent = relationship('Category', remote_side=[id], backref='subcategories')
    products = relationship('Product', secondary=product_categories, back_populates='categories')

class Trend(Base):
    __tablename__ = 'trends'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    source = Column(String(50), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    description = Column(String)
    # Ex: 'BR', 'US', 'EU_GB'
    region = Column(String(10), nullable=False, index=True)
    # Pontuação da tendência, ex: volume de busca
    score = Column(Integer, default=0)
    # Lista de URLs de imagens de inspiração
    inspiration_images = Column(JSON)

    products = relationship('Product', secondary=trend_products, back_populates='trends')

class Store(Base):
    __tablename__ = 'stores'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    logo_url = Column(String)

    products = relationship('Product', back_populates='store')

class Brand(Base):
    __tablename__ = 'brands'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    products = relationship('Product', back_populates='brand')

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    link = Column(String, nullable=False)
    price = Column(String) # Usando String para acomodar "R$ 199,90", "$49.99", etc.
    thumbnail = Column(String)
    
    store_id = Column(Integer, ForeignKey('stores.id'))
    brand_id = Column(Integer, ForeignKey('brands.id'), nullable=True)

    store = relationship('Store', back_populates='products')
    brand = relationship('Brand', back_populates='products')
    trends = relationship('Trend', secondary=trend_products, back_populates='products')
    categories = relationship('Category', secondary=product_categories, back_populates='products')