"""
logic.py
Funciones de validación, ordenamiento y filtrado sobre la lista
de productos en memoria (independientes de la base de datos).
"""


def validar_producto(nombre, precio_texto, stock_texto):
    """
    Valida los datos ingresados por el usuario.
    Devuelve (True, precio, stock) si son válidos,
    o (False, mensaje_error, None) si no lo son.
    """
    if not nombre or not nombre.strip():
        return False, "El nombre no puede estar vacío.", None

    try:
        precio = float(precio_texto)
    except ValueError:
        return False, "El precio debe ser un número.", None

    try:
        stock = int(stock_texto)
    except ValueError:
        return False, "El stock debe ser un número entero.", None

    if precio <= 0:
        return False, "El precio debe ser mayor a 0.", None

    if stock < 0:
        return False, "El stock no puede ser negativo.", None

    return True, precio, stock


def ordenar_por_precio(productos, ascendente=True):
    """Ordena una lista de productos (id, nombre, precio, stock) por precio."""
    return sorted(productos, key=lambda producto: producto[2], reverse=not ascendente)


def ordenar_por_nombre(productos):
    """Ordena alfabéticamente por nombre (necesario antes de la búsqueda binaria)."""
    return sorted(productos, key=lambda producto: producto[1].lower())


def ordenar_por_stock(productos, ascendente=True):
    """Ordena por cantidad en stock."""
    return sorted(productos, key=lambda producto: producto[3], reverse=not ascendente)


def filtrar_stock_bajo(productos, limite=5):
    """Devuelve solo los productos con stock igual o menor al límite dado."""
    return [producto for producto in productos if producto[3] <= limite]


def filtrar_por_nombre(productos, texto):
    """Devuelve los productos cuyo nombre contiene el texto buscado."""
    texto = texto.lower()
    return [producto for producto in productos if texto in producto[1].lower()]
