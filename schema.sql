CREATE TABLE professores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_completo TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    telefone TEXT,
    formacao_academica TEXT,
    areas_especializacao TEXT,
    numero_registro_profissional TEXT,
    experiencia_profissional TEXT,
    foto_de_perfil TEXT
);
