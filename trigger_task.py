# This script triggers the main data pipeline task for all supported regions.
from app.services.tasks import run_product_catalog_sync

if __name__ == "__main__":
    regions = ["BR", "US", "EU"]
    for region in regions:
        print(f"Triggering the product catalog sync task for region: {region}...")
        # .delay() sends the task to the Celery queue to be executed by a worker.
        run_product_catalog_sync.delay(region)
    
    print("All regional tasks sent to the queue. Check the worker's terminal for progress.")