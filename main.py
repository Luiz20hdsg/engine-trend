from fastapi import FastAPI
from app.api.endpoints import trends as catalog_router

# Creates the main FastAPI application instance
app = FastAPI(title="Trend Engine API")

# Includes the catalog router in the main application
# All routes defined in catalog_router.router will be prefixed with /api/v1/catalog
app.include_router(catalog_router.router, prefix="/api/v1/catalog", tags=["Catalog"])

@app.get("/")
def read_root():
    """Root endpoint to check if the API is running."""
    return {"status": "Trend Engine API is running"}