drop database db_poo;

create database db_poo;

use db_poo;

CREATE TABLE registroEstudiante (
    idEstudiante INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    nombreUsuario VARCHAR(50) UNIQUE NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    fechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE registroAdmin (
    idAdmin INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    nombreUsuario VARCHAR(50) UNIQUE NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    fechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cursos (
    idCursos INT AUTO_INCREMENT PRIMARY KEY,
    nombreCurso VARCHAR(100) NOT NULL,  -- Nombre del curso
    descripcion TEXT,
    categoria ENUM('digital', 'analogico') NOT NULL,
    fechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    imagen VARCHAR(255),
    precio VARCHAR(10) NOT NULL
);
INSERT INTO cursos (nombreCurso, descripcion, categoria, fechaCreacion, imagen, precio)
VALUES (
    'Curso de Programación en Python', 
    'Curso de programación en Python desde cero, cubriendo conceptos básicos hasta avanzados.',
    'digital',
    NOW(), 
    'static/images/python_course.jpg', 
    99.99  
);
INSERT INTO cursos (nombreCurso, descripcion, categoria, fechaCreacion, imagen, precio)
VALUES (
    'DISEÑO DE COMPUTADORAS', 
    'Se desarrollará un CPU desde cero',
    'digital',
    NOW(), 
    'static/images/compu_course.jpg',
    199.99 
);
INSERT INTO cursos (nombreCurso, descripcion, categoria, fechaCreacion, imagen, precio)
VALUES (
    'ÑÑÑÓÓ', 
    'Se desarrollará un CPU desde cero',
    'analogico',
    NOW(), 
    'static/images/aa_course.jpg',
    100.00 
);

INSERT INTO cursos (nombreCurso, descripcion, categoria, fechaCreacion, imagen, precio)
VALUES (
    'ÑÑÑÓ', 
    'Se desarrollará un CPU desde cero',
    'analogico',
    NOW(), 
    'static/images/xd_course.jpg',
    200.00 
);

CREATE TABLE compras (
    idCompra INT AUTO_INCREMENT PRIMARY KEY,
    idEstudiante INT NOT NULL,
    idCursos INT NOT NULL,
    fechaCompra DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('GRATIS', 'PAGADO') NOT NULL,
    FOREIGN KEY (idEstudiante) REFERENCES registroEstudiante(idEstudiante),
    FOREIGN KEY (idCurso) REFERENCES cursos(idCurso)
);