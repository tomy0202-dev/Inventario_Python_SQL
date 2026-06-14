import os
import psycopg2

conexion = psycopg2.connect(
    os.environ.get("DATABASE_URL")
)
cursor = conexion.cursor()

# borrar tabla si existe
cursor.execute("""
DROP TABLE IF EXISTS administradores
""")

# crear tabla correcta
cursor.execute("""
CREATE TABLE administradores (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(100) UNIQUE NOT NULL,
    clave VARCHAR(255) NOT NULL

)
""")

# crear admin
cursor.execute("""
INSERT INTO administradores
(usuario, clave)
VALUES
('admin', '1234')
""")
conexion.commit()

cursor.close()
conexion.close()
print("Tabla administradores creada")