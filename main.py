from fastapi import FastAPI
from app.api.endpoints import trends, stores, brands

# Cria a instância principal da aplicação FastAPI
app = FastAPI(title="Trend Engine API")

# Inclui o roteador de tendências na aplicação principal
# Todas as rotas definidas em trends.router serão prefixadas com /api/v1
app.include_router(trends.router, prefix="/api/v1", tags=["Trends"])
app.include_router(stores.router, prefix="/api/v1", tags=["Stores"])
app.include_router(brands.router, prefix="/api/v1", tags=["Brands"])

@app.get("/")
def read_root():
    """Endpoint raiz para verificar se a API está no ar."""
    return {"status": "Trend Engine API is running"}
