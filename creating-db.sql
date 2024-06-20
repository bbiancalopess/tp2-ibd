-- Criação da tabela Mesorregião
CREATE TABLE mesorregioes (
    id SERIAL PRIMARY KEY,
    nome_mesorregiao VARCHAR(255) NOT NULL
);

-- Criação da tabela Municípios com a chave estrangeira para Mesorregião
CREATE TABLE municipios (
    id SERIAL PRIMARY KEY,
    nome_municipio VARCHAR(255) NOT NULL,
    id_mesorregiao INTEGER NOT NULL,
    mortalidade_geral FLOAT,
    mortalidade_feminina FLOAT,
    mortalidade_masculina FLOAT,
    pib FLOAT,
    populacao INTEGER,
    CONSTRAINT fk_mesoregioes FOREIGN KEY(id_mesorregiao) REFERENCES mesorregioes(id)
);

