from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session

import mysql.connector

app = Flask(__name__)

# Clave sesión
app.secret_key = "inventario2026"

# Conexión BD
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="0202",
        database="inventario"
    )

# Verificar login
def protegido():
    return session.get(
        "login"
    )

# LOGIN
@app.route(
"/login",
methods=[
"GET",
"POST"
]
)

def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        clave = request.form["clave"]
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute(
            """
            SELECT *
            FROM administradores
            WHERE usuario=%s
            AND clave=%s
            """,
            (
                usuario,
                clave
            )
        )
        admin = cursor.fetchone()
        cursor.close()
        conexion.close()
        if admin:
            session["login"] = True
            return redirect("/")
    return render_template(
        "login.html"
    )

# LOGOUT
@app.route(
"/logout"
)
def logout():
    session.clear()
    return redirect(
        "/login"
    )

# INICIO
@app.route("/")
def inicio():
    if not protegido():
        return redirect(
            "/login"
        )
    return render_template(
        "index.html"
    )

# AGREGAR
@app.route(
"/agregar",
methods=[
"GET",
"POST"
]
)
def agregar():
    if not protegido():
        return redirect(
            "/login"
        )
    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = request.form["precio"]
        cantidad = request.form["cantidad"]
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute(
            """
            INSERT INTO productos
            (
            nombre,
            precio,
            cantidad
            )

            VALUES

            (
            %s,
            %s,
            %s
            )
            """,
            (
                nombre,
                precio,
                cantidad
            )
        )
        conexion.commit()
        cursor.close()
        conexion.close()
        return redirect(
            "/inventario"
        )
    return render_template(
        "agregar.html"
    )

# INVENTARIO
@app.route(
"/inventario"
)
def inventario():
    if not protegido():
        return redirect(
            "/login"
        )
    busqueda = request.args.get(
        "buscar",
        ""
    )
    conexion = conectar()
    cursor = conexion.cursor()
    if busqueda:
        cursor.execute(
            """
            SELECT *
            FROM productos
            WHERE nombre
            LIKE %s
            """,
            (
                f"%{busqueda}%",
            )
        )
    else:
        cursor.execute(
            "SELECT * FROM productos"
        )
    productos = cursor.fetchall()
    cursor.execute(
        """
        SELECT

        COUNT(*),

        SUM(
        precio*cantidad
        )

        FROM productos
        """
    )
    resumen = cursor.fetchone()
    total = resumen[0]
    valor = resumen[1] or 0
    valor = f"{valor:,.0f}"
    cursor.close()
    conexion.close()
    return render_template(
        "inventario.html",
        productos=productos,
        total=total,
        valor=valor
    )

# ELIMINAR
@app.route(
"/eliminar/<int:id_producto>"
)
def eliminar(id_producto):
    if not protegido():
        return redirect(
            "/login"
        )
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        """
        DELETE
        FROM productos
        WHERE id=%s
        """,
        (
            id_producto,
        )
    )
    conexion.commit()
    cursor.close()
    conexion.close()
    return redirect(
        "/inventario"
    )

# ACTUALIZAR
@app.route(
"/actualizar",
methods=[
"GET",
"POST"
]
)
def actualizar():
    if not protegido():
        return redirect(
            "/login"
        )
    if request.method == "POST":
        id_producto = request.form["id"]
        cantidad = request.form["cantidad"]
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute(
            """
            UPDATE productos

            SET cantidad=%s

            WHERE id=%s
            """,
            (
                cantidad,
                id_producto
            )
        )
        conexion.commit()
        cursor.close()
        conexion.close()
        return redirect(
            "/inventario"
        )
    return render_template(
        "actualizar.html"
    )

app.run(
debug=True
)