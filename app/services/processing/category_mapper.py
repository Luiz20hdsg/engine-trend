from typing import Union

"""
Mapeia as categorias específicas da fonte para os slugs de categoria internos do sistema.
"""

# Este dicionário é o ponto central para traduzir as categorias.
# Chave: Nome da categoria vinda da fonte (em maiúsculas e com underscores).
# Valor: Slug correspondente na tabela 'categories' do banco de dados.
CATEGORY_MAP = {
    # Mapeamentos da fonte para o slug
    'GENERAL': 'acessorios',
    'APPAREL_ACCESSORIES': 'acessorios',
    'BEAUTY_PERSONAL_CARE': 'beleza',
    'FASHION': 'acessorios',

    # Mapeamentos de slugs para eles mesmos (para robustez)
    'READY_TO_WEAR': 'ready-to-wear',
    'ACESSORIOS': 'acessorios',
    'BELEZA': 'beleza',
    'VESTIDOS': 'vestidos',
    'CAMISAS_E_BLUSAS': 'camisas-e-blusas',
    'CALCAS_E_SHORTS': 'calcas-e-shorts',
}

def get_mapped_category_slug(source_category: str) -> Union[str, None]:
    """
    Traduz uma categoria de uma fonte de dados para um slug de categoria do sistema.

    :param source_category: A string da categoria vinda da fonte (ex: 'APPAREL_ACCESSORIES').
    :return: O slug correspondente do sistema (ex: 'acessorios') ou None se não houver mapeamento.
    """
    if not source_category:
        return None
    # Converte para maiúsculas e substitui hífens por underscores para consistência da chave
    processed_key = source_category.upper().replace('-', '_')
    return CATEGORY_MAP.get(processed_key)
