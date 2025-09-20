web: PYTHONPATH=. gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
worker: PYTHONPATH=. celery -A app.core.celery_app.celery_app worker --loglevel=info
