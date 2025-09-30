-- Drop existing tables in reverse order of creation to handle dependencies
DROP TABLE IF EXISTS trend_products;
DROP TABLE IF EXISTS product_categories;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS trends;
DROP TABLE IF EXISTS brands;
DROP TABLE IF EXISTS stores;
DROP TABLE IF EXISTS categories;
DROP TYPE IF EXISTS region_enum;
DROP TABLE IF EXISTS filters;
DROP TABLE IF EXISTS search_queries;

-- Enum for the supported regions
CREATE TYPE region_enum AS ENUM ('BR', 'US', 'EU');

-- Tabela para armazenar as consultas de busca que o robô usará.
CREATE TABLE search_queries (
    id SERIAL PRIMARY KEY,
    query VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    region region_enum NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(query, region) -- A mesma query pode existir para diferentes regiões
);

-- Tabela para armazenar os filtros extraídos para cada consulta.
CREATE TABLE filters (
    id SERIAL PRIMARY KEY,
    search_query_id INTEGER NOT NULL REFERENCES search_queries(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(search_query_id, name)
);

-- Tabela principal de produtos, otimizada para o catálogo do app.
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    google_product_id VARCHAR(255) UNIQUE NOT NULL,
    search_query_id INTEGER NOT NULL REFERENCES search_queries(id) ON DELETE CASCADE,
    region region_enum NOT NULL,
    title VARCHAR(512) NOT NULL,
    brand VARCHAR(255),
    price NUMERIC(10, 2),
    thumbnail_url TEXT,
    store_name VARCHAR(255),
    store_link TEXT NOT NULL,
    rating NUMERIC(3, 2),
    reviews INTEGER,
    variants JSONB,
    other_details JSONB,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Índices
CREATE INDEX idx_products_region_category ON products(region, search_query_id);
CREATE INDEX idx_products_brand ON products(brand);
CREATE INDEX idx_products_price ON products(price);

-- Inserir buscas para o Brasil (BR)
INSERT INTO search_queries (query, category, region) VALUES
-- Lojas
('site:dafiti.com.br', 'fashion-store', 'BR'),
('site:netshoes.com.br', 'fitness-store', 'BR'),
('site:zattini.com.br', 'fashion-store', 'BR'),
('site:farmrio.com.br', 'fashion-store', 'BR'),
('site:amaro.com', 'fashion-store', 'BR'),
('site:lojasrenner.com.br', 'fashion-store', 'BR'),
('site:cea.com.br', 'fashion-store', 'BR'),
('Reserva', 'fashion-store', 'BR'),
('Riachuelo', 'fashion-store', 'BR'),
('Zara', 'fashion-store', 'BR'),
('Nike', 'fitness-store', 'BR'),
('Adidas', 'fitness-store', 'BR'),
('Shein', 'fashion-store', 'BR'),
('Shopee', 'general-store', 'BR'),
('Farfetch', 'luxury-store', 'BR'),
('Amazon', 'general-store', 'BR'),
-- Categorias Temáticas
('skincare', 'beauty', 'BR'),
('fitness suplemento', 'fitness', 'BR'),
('produto de beleza', 'beauty', 'BR'),
('relógios', 'accessories', 'BR'),
('joias', 'jewelry', 'BR'),
('bijuterias finas', 'jewelry', 'BR'),
('bijuterias', 'jewelry', 'BR'),
('acessórios femininos', 'accessories', 'BR'),
('acessórios masculinos', 'accessories', 'BR'),
('oculos', 'accessories', 'BR'),
('bones', 'accessories', 'BR'),
('chapeus', 'accessories', 'BR'),
('bolsas', 'bags', 'BR'),
('bolsas de mão', 'bags', 'BR'),
('bolsas de ombro', 'bags', 'BR'),
('bolsas tote', 'bags', 'BR'),
('bolsas hobo', 'bags', 'BR'),
('bolsas mini', 'bags', 'BR'),
('tênis', 'footwear', 'BR'),
('sandálias', 'footwear', 'BR'),
('sapatilhas', 'footwear', 'BR'),
('mocassins', 'footwear', 'BR'),
('pumps', 'footwear', 'BR'),
('botas', 'footwear', 'BR'),
('vestidos', 'apparel', 'BR'),
('camisas e blusas', 'apparel', 'BR'),
('camisetas e moletons', 'apparel', 'BR'),
('tricô', 'apparel', 'BR'),
('saias', 'apparel', 'BR'),
('calças e shorts', 'apparel', 'BR'),
('denim', 'apparel', 'BR'),
('roupas íntimas', 'apparel', 'BR'),
('roupa de banho', 'apparel', 'BR'),
('agasalhos', 'apparel', 'BR'),
('casacos e jaquetas', 'apparel', 'BR'),
('acessórios para bolsas', 'accessories', 'BR'),
('chapéus e luvas', 'accessories', 'BR'),
('acessórios para cabelo', 'accessories', 'BR'),
('óculos', 'accessories', 'BR'),
('echarpes e meias', 'accessories', 'BR'),
('cintos', 'accessories', 'BR'),
('nécessaires', 'accessories', 'BR'),
('carteiras', 'accessories', 'BR'),
('porta-cartões', 'accessories', 'BR'),
('brincos', 'jewelry', 'BR'),
('pulseiras', 'jewelry', 'BR'),
('colares', 'jewelry', 'BR'),
('anéis', 'jewelry', 'BR');

-- Placeholder para outras regiões
INSERT INTO search_queries (query, category, region) VALUES
('Sephora', 'beauty-store', 'US'),
('Nike', 'fitness-store', 'US'),
('ASOS', 'fashion-store', 'EU'),
('Zalando', 'fashion-store', 'EU');