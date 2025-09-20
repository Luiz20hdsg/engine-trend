import time
from sqlalchemy import text
from app.database.session import SessionLocal
from app.database.models import product_categories


def check_product_categories_count():
    db = SessionLocal()
    try:
        # Espera um pouco para dar tempo ao worker de processar os dados
        print("Aguardando 120 segundos para o processamento dos dados...")
        time.sleep(120)

        print("Verificando o número de registros na tabela 'product_categories'...")
        
        # Usando a tabela de associação diretamente para contar as linhas
        count = db.query(product_categories).count()
        
        if count > 0:
            print(f"\nSUCESSO! A tabela 'product_categories' agora contém {count} registros.")
            print("A associação entre produtos e categorias está funcionando.")
        else:
            print(f"\nFALHA. A tabela 'product_categories' ainda está vazia.")
            print("Pode ser necessário mais tempo para o processamento ou o problema persiste.")
            
    except Exception as e:
        print(f"Ocorreu um erro durante a verificação: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_product_categories_count()
