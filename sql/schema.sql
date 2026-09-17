-- TABLA CATEGORIAS
CREATE TABLE categorias (
    id_categoria SERIAL PRIMARY KEY,
    categoria VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- TABLA DE CLIENTES
CREATE TABLE clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE,
    fecha_registro DATE,
    region VARCHAR(100)
);

-- TABLA DE MÉTODOS DE PAGO
CREATE TABLE metodos_pago (
    id_metodo SERIAL PRIMARY KEY,
    metodo VARCHAR(50) NOT NULL,
    descripcion TEXT
);

-- TABLA DE PRODUCTOS (incluye el stock)
CREATE TABLE productos (
    id_producto SERIAL PRIMARY KEY,
    nombre_producto VARCHAR(200) NOT NULL,
    id_categoria INT REFERENCES categorias(id_categoria),
    precio_unitario DECIMAL (10, 2) NOT NULL CHECK (precio_unitario > 0),
    stock INT NOT NULL DEFAULT 0 CHECK (stock >=0)
);

-- TABLA DE VENTAS (Tabla de hechos unificada)
CREATE TABLE ventas (
    id_venta SERIAL PRIMARY KEY,
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_cliente INT REFERENCES clientes(id_cliente),
    id_producto INT REFERENCES productos(id_producto),
    cantidad INT NOT NULL CHECK (cantidad >0),
    id_metodo INT REFERENCES metodos_pago(id_metodo),
    estado VARCHAR(50) CHECK (estado IN ('Completa', 'Pendiente', 'Cancelada'))
);