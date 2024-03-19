-- Criação da tabela 'products'
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    product_id BIGINT,
    name VARCHAR(450),
    sn VARCHAR(50),
    url TEXT,
    imgs TEXT,
    category VARCHAR(400),
    store_code BIGINT,
    is_on_sale BOOLEAN,
    price_real_symbol VARCHAR(20),
    price_real NUMERIC(10, 2),
    price_us_symbol VARCHAR(20),
    price_us NUMERIC(10, 2),
    discount_price_real_symbol VARCHAR(20),
    discount_price_real NUMERIC(10, 2),
    discount_price_us_symbol VARCHAR(20),
    discount_price_us NUMERIC(10, 2),
    datetime_collected TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



-- Criação da tabela 'price_history'
-- Criação da tabela 'price_history'
CREATE TABLE IF NOT EXISTS price_history (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    price NUMERIC(10, 2),
    price_real_symbol VARCHAR(20),
    price_real NUMERIC(10, 2),
    price_us_symbol VARCHAR(20),
    price_us NUMERIC(10, 2),
    discount_price_real_symbol VARCHAR(20),
    discount_price_real NUMERIC(10, 2),
    discount_price_us_symbol VARCHAR(20),
    discount_price_us NUMERIC(10, 2),
    product_id INTEGER REFERENCES products(id)
);



