from slugify import slugify
from app.database.session import SessionLocal, engine
from app.database.models import Base, Category

# Apaga e recria as tabelas para garantir o schema mais recente
print("Apagando tabelas existentes...")
Base.metadata.drop_all(bind=engine)
print("Tabelas apagadas.")
print("Criando novas tabelas...")
Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso.")

# Os dados que queremos inserir
CATEGORIES_DATA = {
    "READY TO WEAR": [
        "VESTIDOS", "CAMISAS E BLUSAS", "CAMISETAS E MOLETONS", "TRICÔ", "SAIAS",
        "CALÇAS E SHORTS", "DENIM", "ROUPAS ÍNTIMAS E DE BANHO", "AGASALHOS",
        "CASACOS E JAQUETAS"
    ],
    "ACESSÓRIOS": [
        "ACESSÓRIOS PARA BOLSAS E CHAVEIROS", "CHAPÉUS E LUVAS",
        "TIARAS E ACESSÓRIOS PARA CABELO", "ÓCULOS", "ECHARPES E MEIAS", "CINTOS",
        "NÉCESSAIRES"
    ],
    "BIJUTERIAS FINAS": ["BRINCOS", "PULSEIRAS", "COLARES", "ANÉIS E BROCHES"],
    "CALÇADOS": [],
    "BOLSAS": [],
    "BELEZA": [],
}

def seed_categories():
    db = SessionLocal()
    try:
        # Limpa as categorias existentes para evitar duplicatas
        num_deleted = db.query(Category).delete()
        if num_deleted > 0:
            print(f"{num_deleted} categorias antigas foram removidas.")

        print("Inserindo novas categorias...")

        for parent_name, children_names in CATEGORIES_DATA.items():
            # Cria a categoria pai
            parent_slug = slugify(parent_name)
            parent_category = Category(name=parent_name, slug=parent_slug)
            db.add(parent_category)
            db.flush()  # Usa flush para obter o ID do pai antes de commitar

            # Cria as categorias filhas
            for child_name in children_names:
                child_slug = slugify(child_name)
                child_category = Category(
                    name=child_name,
                    slug=child_slug,
                    parent_id=parent_category.id
                )
                db.add(child_category)
        
        db.commit()
        print("Categorias inseridas com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Iniciando o processo de popular o banco de dados com categorias...")
    seed_categories()
