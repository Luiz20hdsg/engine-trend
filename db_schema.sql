-- Enum para as regiões suportadas
CREATE TYPE region_enum AS ENUM ('BR', 'US', 'EU');

-- Tabela de Categorias (hierárquica)
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    parent_id INTEGER REFERENCES categories(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Tabela de Lojas
CREATE TABLE stores (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    domain VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Tabela de Marcas
CREATE TABLE brands (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Tabela de Tendências
CREATE TABLE trends (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    region region_enum NOT NULL,
    score INTEGER DEFAULT 0, -- Pontuação para ordenar a relevância
    images_urls JSONB, -- URLs das imagens de inspiração
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(name, region) -- Uma tendência é única por nome e região
);

-- Tabela de Produtos
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    title VARCHAR(512) NOT NULL,
    link TEXT NOT NULL,
    price VARCHAR(100),
    thumbnail_url TEXT,
    store_id INTEGER NOT NULL REFERENCES stores(id),
    brand_id INTEGER REFERENCES brands(id),
    region region_enum NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(link) -- O link do produto é um identificador único
);

-- Tabela de Ligação: Produtos <-> Categorias (Muitos para Muitos)
CREATE TABLE product_categories (
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    PRIMARY KEY (product_id, category_id)
);

-- Tabela de Ligação: Produtos <-> Tendências (Muitos para Muitos)
CREATE TABLE trend_products (
    trend_id INTEGER NOT NULL REFERENCES trends(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    PRIMARY KEY (trend_id, product_id)
);

-- Índices para otimizar as buscas
CREATE INDEX idx_trends_region_score ON trends(region, score DESC);
CREATE INDEX idx_products_region ON products(region);
