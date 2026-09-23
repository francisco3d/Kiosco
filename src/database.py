"""
database.py
Módulo encargado de la conexión con la base de datos SQLite
y de las operaciones básicas sobre las tablas de productos y ventas.
"""

import sqlite3
import os

# Ruta absoluta a la base de datos, sin importar desde dónde se ejecute el programa
RUTA_BASE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "kiosco.db"
)


def conectar():
    """Abre (o crea) la conexión con la base de datos."""
    return sqlite3.connect(RUTA_BASE)


def crear_tabla():
    """Crea las tablas de productos y ventas si no existen todavía."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            total REAL NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
    """)
    conexion.commit()
    conexion.close()


def alta_producto(nombre, precio, stock):
    """Inserta un producto nuevo."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
        (nombre, precio, stock),
    )
    conexion.commit()
    conexion.close()


def consultar_todos():
    """Devuelve todos los productos como lista de tuplas (id, nombre, precio, stock)."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, precio, stock FROM productos")
    resultados = cursor.fetchall()
    conexion.close()
    return resultados


def buscar_por_id(id_producto):
    """Devuelve un único producto por su id, o None si no existe."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT id, nombre, precio, stock FROM productos WHERE id = ?",
        (id_producto,),
    )
    resultado = cursor.fetchone()
    conexion.close()
    return resultado


def modificar_producto(id_producto, nombre, precio, stock):
    """Actualiza nombre, precio y stock de un producto existente."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE productos SET nombre = ?, precio = ?, stock = ? WHERE id = ?",
        (nombre, precio, stock, id_producto),
    )
    conexion.commit()
    conexion.close()


def eliminar_producto(id_producto):
    """Borra un producto por su id."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
    conexion.commit()
    conexion.close()


def actualizar_stock(id_producto, nuevo_stock):
    """Actualiza solo el stock de un producto (usado al vender)."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE productos SET stock = ? WHERE id = ?", (nuevo_stock, id_producto)
    )
    conexion.commit()
    conexion.close()


def consultar_ventas():
    """
    Devuelve todas las ventas registradas, con el nombre del producto incluido,
    ordenadas de la más vieja a la más nueva.
    Cada elemento: (id_venta, nombre_producto, cantidad, total, fecha).
    """
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT ventas.id, productos.nombre, ventas.cantidad, ventas.total, ventas.fecha
        FROM ventas
        JOIN productos ON productos.id = ventas.producto_id
        ORDER BY ventas.id ASC
    """)
    resultados = cursor.fetchall()
    conexion.close()
    return resultados


def registrar_venta(producto_id, cantidad, total, fecha):
    """Guarda un registro de venta en la tabla de ventas."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO ventas (producto_id, cantidad, total, fecha) VALUES (?, ?, ?, ?)",
        (producto_id, cantidad, total, fecha),
    )
    conexion.commit()
    conexion.close()
