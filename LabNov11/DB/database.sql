#nombre: database.sql
drop database db_poo; #eliminar base de daotos en caso de que exista
create database db_poo;

use db_poo;

CREATE TABLE usuarios (
    codigo INT PRIMARY KEY AUTO_INCREMENT,
    nombres VARCHAR(100) NOT NULL,
    login VARCHAR(50) UNIQUE NOT NULL,
    clave VARCHAR(255) NOT NULL,
    tipo ENUM('admin', 'user', 'guest') NOT NULL
);


#Datos de prueba
INSERT INTO usuarios (nombres, login, clave, tipo) VALUES
('Juan Pérez', 'juanperez', 'password123', 'profesor'),
('Ana Gómez', 'anagomez', 'pass456', 'alumno'),
('Luis Salas', 'luissalas', 'clave789', 'alumno');