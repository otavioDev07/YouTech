CREATE TABLE IF NOT EXISTS vagas (
    id INTEGER PRIMARY KEY,
    cargo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    requisitos TEXT NOT NULL,
    img TEXT NOT NULL, 
    modalidade TEXT NOT NULL,
    local TEXT NOT NULL,
    salario REAL NOT NULL,
    email TEXT NOT NULL,
    setor TEXT NOT NULL
);  