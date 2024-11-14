CREATE TABLE IF NOT EXISTS usuarios (
    codigo SERIAL PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    login VARCHAR(50) UNIQUE NOT NULL,
    clave VARCHAR(255) NOT NULL,
    tipo VARCHAR(10) CHECK (tipo IN ('alumno', 'profesor')) NOT NULL
);
