"""
estructuras.py
Contiene el Tipo de Dato Abstracto (Pila) usado para el historial
de ventas, y la función recursiva de búsqueda binaria de productos.
"""


class Pila:
    """
    TDA Pila (stack) - estructura LIFO (el último que entra es el primero
    que sale). Se usa para guardar el historial de las ventas realizadas,
    de forma que la venta más reciente quede siempre "arriba".
    """

    def __init__(self):
        self._elementos = []

    def apilar(self, elemento):
        """Agrega un elemento arriba de la pila."""
        self._elementos.append(elemento)

    def desapilar(self):
        """Quita y devuelve el elemento de arriba. Devuelve None si está vacía."""
        if self.esta_vacia():
            return None
        return self._elementos.pop()

    def ver_tope(self):
        """Devuelve el elemento de arriba sin quitarlo."""
        if self.esta_vacia():
            return None
        return self._elementos[-1]

    def esta_vacia(self):
        return len(self._elementos) == 0

    def tamanio(self):
        return len(self._elementos)

    def como_lista(self):
        """Devuelve las ventas de la más reciente a la más antigua."""
        return list(reversed(self._elementos))


def busqueda_binaria_recursiva(lista_productos, nombre_buscado, inicio=0, fin=None):
    """
    Busca un producto por nombre usando búsqueda binaria recursiva.
    Requiere que 'lista_productos' esté ordenada alfabéticamente por nombre
    (ver logic.ordenar_por_nombre).

    lista_productos: lista de tuplas (id, nombre, precio, stock)
    Devuelve la tupla del producto encontrado, o None si no existe.
    """
    if fin is None:
        fin = len(lista_productos) - 1

    # Caso base: no quedan elementos para revisar
    if inicio > fin:
        return None

    medio = (inicio + fin) // 2
    nombre_medio = lista_productos[medio][1].lower()
    nombre_buscado = nombre_buscado.lower()

    if nombre_medio == nombre_buscado:
        return lista_productos[medio]
    elif nombre_buscado < nombre_medio:
        # Caso recursivo: buscar en la mitad izquierda
        return busqueda_binaria_recursiva(lista_productos, nombre_buscado, inicio, medio - 1)
    else:
        # Caso recursivo: buscar en la mitad derecha
        return busqueda_binaria_recursiva(lista_productos, nombre_buscado, medio + 1, fin)
