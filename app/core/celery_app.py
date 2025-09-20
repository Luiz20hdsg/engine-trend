from celery import Celery
from app.core.config import settings

# Cria a instância do Celery
# O primeiro argumento é o nome do módulo atual.
# O broker é a URL do Redis onde o Celery enviará as mensagens de tarefa.
# O backend é onde o Celery armazenará os resultados das tarefas.
celery_app = Celery(
    "trend_engine_worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.services.tasks"]  # Lista de módulos onde o Celery deve procurar por tarefas
)

# Configurações opcionais
celery_app.conf.update(
    task_track_started=True,
    # Outras configurações podem ser adicionadas aqui
)
