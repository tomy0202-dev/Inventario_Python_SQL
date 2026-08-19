import os
import psycopg2

conexion = psycopg2.connect(
    os.environ.get("DATABASE_URL")
)

cursor = conexion.cursor()

# Crear tabla administradores
cursor.execute("""
CREATE TABLE IF NOT EXISTS administradores (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(100) UNIQUE NOT NULL,
    clave VARCHAR(255) NOT NULL
)
""")

# Crear administrador
cursor.execute("""
INSERT INTO administradores (usuario, clave)
VALUES ('admin', '1234')
ON CONFLICT (usuario) DO NOTHING
""")

# Crear tabla productos
cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio NUMERIC(12,2) NOT NULL,
    cantidad INTEGER NOT NULL
)
""")

conexion.commit()

cursor.close()
conexion.close()

print("Base de datos creada correctamente")
