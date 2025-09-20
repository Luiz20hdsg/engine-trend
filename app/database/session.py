from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Cria a engine do SQLAlchemy usando a URL do banco de dados das configurações
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Cria uma fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)