import requests
import json
from app.core.config import settings
from app.core.celery_app import celery_app
from app.database.session import SessionLocal
from app.crud import crud_trends as crud_catalog
from app.schemas import trend as catalog_schema

# I'm keeping the service and tasks in the same file for now.
# In a real-world scenario, hasdata_service would be in its own file.

HASDATA_API_URL = "https://api.hasdata.com/scrape/google"

# Mapping for region-specific parameters for the Hasdata API
REGION_PARAMS = {
    "BR": {"location": "Brazil", "gl": "br", "hl": "pt-br"},
    "US": {"location": "United States", "gl": "us", "hl": "en"},
    "EU": {"location": "Germany", "gl": "de", "hl": "de"}, # Using Germany as a proxy for EU
}

def get_shopping_results(query: str, region: str = "BR") -> dict:
    """
    Calls the Hasdata Google Shopping API for a specific region.
    """
    if not settings.HASDATA_API_KEY:
        print("Error: HASDATA_API_KEY not configured.")
        return {}

    region_upper = region.upper()
    if region_upper not in REGION_PARAMS:
        print(f"Error: Region '{region}' not supported.")
        return {}

    url = f"{HASDATA_API_URL}/shopping"
    params = {
        "q": query,
        "deviceType": "desktop",
        **REGION_PARAMS[region_upper]
    }
    headers = {
        "Content-Type": "application/json",
        "x-api-key": settings.HASDATA_API_KEY,
    }

    try:
        print(f"Calling Hasdata Shopping API for query='{query}' in region='{region_upper}'")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Hasdata Shopping API: {e}")
        return {}

def get_immersive_details(page_token: str) -> dict:
    """
    Calls the Hasdata Google Immersive Product API.
    """
    if not settings.HASDATA_API_KEY:
        print("Error: HASDATA_API_KEY not configured.")
        return {}

    url = f"{HASDATA_API_URL}/immersive-product"
    params = {"pageToken": page_token}
    headers = {
        "Content-Type": "application/json",
        "x-api-key": settings.HASDATA_API_KEY,
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Hasdata Immersive Product API: {e}")
        return {}


@celery_app.task(acks_late=True)
def fetch_and_save_product_details(product_data: dict, search_query_id: int, region: str):
    """
    Sub-task to fetch immersive details for a single product and save it.
    """
    print(f"Fetching details for product: {product_data.get('title')}")
    page_token = product_data.get("immersiveProductPageToken")
    if not page_token:
        return

    details = get_immersive_details(page_token=page_token)
    product_results = details.get("productResults")

    if not product_results:
        return

    store_info = product_results.get("stores", [])[0] if product_results.get("stores") else {}
    if not store_info:
        return

    # Ensure the product has the required fields
    if not (product_data.get("productId") and store_info.get("link")):
        return

    product_to_save = catalog_schema.ProductCreate(
        google_product_id=product_data.get("productId"),
        search_query_id=search_query_id,
        region=region.upper(),
        title=product_results.get("title"),
        brand=product_results.get("brand"),
        price=store_info.get("extractedPrice"),
        thumbnail_url=product_results.get("thumbnails", [])[0] if product_results.get("thumbnails") else None,
        store_name=store_info.get("name"),
        store_link=store_info.get("link"),
        rating=product_results.get("rating"),
        reviews=product_results.get("reviews"),
        variants=product_results.get("variants"),
        other_details={
            "price_range": product_results.get("priceRange"),
            "details_and_offers": store_info.get("detailsAndOffers"),
        },
    )

    db = SessionLocal()
    try:
        crud_catalog.create_or_update_product(db, product=product_to_save)
        print(f"Saved product: {product_to_save.title}")
    finally:
        db.close()


@celery_app.task(acks_late=True)
def run_product_catalog_sync(region: str):
    """
    Main task to sync the product catalog from Hasdata for a specific region.
    """
    print(f"--- Starting Product Catalog Sync for region: {region.upper()} ---")
    db = SessionLocal()
    try:
        search_queries = crud_catalog.get_active_search_queries_by_region(db, region=region)
        print(f"Found {len(search_queries)} active search queries for region {region.upper()}.")

        for sq in search_queries:
            print(f"Processing query: '{sq.query}'")
            shopping_results = get_shopping_results(query=sq.query, region=sq.region)

            if not shopping_results:
                print(f"No results for query: '{sq.query}'")
                continue

            # --- Filter Extraction ---
            filters_data = shopping_results.get("filters", [])
            for filter_group in filters_data:
                filter_type = filter_group.get("title")
                for filter_option in filter_group.get("options", []):
                    filter_name = filter_option.get("text")
                    if filter_name:
                        crud_catalog.get_or_create_filter(db, search_query_id=sq.id, name=filter_name, type=filter_type)
            print(f"Extracted and saved filters for '{sq.query}'.")

            # --- Product Fetching ---
            products = shopping_results.get("shoppingResults", [])
            print(f"Found {len(products)} products for '{sq.query}'. Dispatching sub-tasks...")
            for product in products:
                fetch_and_save_product_details.delay(product_data=product, search_query_id=sq.id, region=sq.region)

    finally:
        db.close()
    print(f"--- Product Catalog Sync Finished for region: {region.upper()} ---")