# Este script dispara a tarefa inicial do nosso pipeline de dados.
from app.services.tasks import collect_and_process_trends

if __name__ == "__main__":
    print("Disparando a tarefa de coleta e processamento para a região 'BR'...")
    # .delay() envia a tarefa para a fila do Celery para ser executada por um worker.
    collect_and_process_trends.delay('BR')
    print("Tarefa enviada para a fila. Verifique o terminal do worker para ver o progresso.")
