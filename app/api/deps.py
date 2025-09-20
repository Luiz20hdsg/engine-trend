from app.database.session import SessionLocal

def get_db():
    """Dependência do FastAPI para obter uma sessão de banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
