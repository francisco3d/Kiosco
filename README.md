# Kiosco - Olimpíadas de Programación (5° año)

Aplicación de escritorio para gestionar el stock y las ventas de un kiosco,
desarrollada en Python con Tkinter (interfaz) y SQLite (persistencia).

## Cómo ejecutar

```bash
python main.py
```

No hace falta instalar nada externo: usa solo el estándar de Python
(`tkinter`, `sqlite3`, `datetime`).

## Estructura del proyecto

```
mi_proyecto_pc/
├── src/
│   ├── __init__.py
│   ├── database.py      # Conexión, tablas y operaciones CRUD con SQLite
│   ├── estructuras.py   # TDA Pila (historial de ventas) + búsqueda binaria recursiva
│   ├── logic.py         # Validaciones, ordenamientos y filtros
│   └── gui.py           # Interfaz gráfica (Tkinter)
├── assets/               # Íconos/imágenes (opcional)
├── main.py               # Punto de entrada
├── requirements.txt
├── .gitignore
└── README.md
```

## Funcionalidades

- Alta, modificación y eliminación de productos.
- Búsqueda de un producto por nombre (búsqueda binaria recursiva).
- Ordenamiento de productos por precio.
- Filtrado de productos con stock bajo (≤5 unidades).
- Registro de ventas con descuento automático de stock.
- Historial de ventas de la sesión (TDA Pila, orden LIFO).
- Validación de los datos ingresados (nombre, precio, stock).

## Requisitos de la consigna cubiertos

| Requisito de la olimpíada                     | Dónde está implementado                          |
|------------------------------------------------|---------------------------------------------------|
| Programación estructurada / funciones          | `database.py`, `logic.py`, `gui.py`                |
| Listas / arreglos                              | Listas de tuplas devueltas desde la base de datos  |
| Tipo de Dato Abstracto                         | Clase `Pila` en `estructuras.py`                   |
| Función recursiva aplicada a algo real          | `busqueda_binaria_recursiva` en `estructuras.py`   |
| Alta / consulta / modificación / eliminación    | Botones de `gui.py` + funciones de `database.py`   |
| Búsqueda, ordenamiento y filtrado               | Botones de `gui.py` + funciones de `logic.py`      |
| Validación de datos                            | `logic.py` → `validar_producto`                    |

## Posibles ampliaciones (por si el jurado pide algo nuevo)

- Agregar una tabla de "proveedores" y relacionarla con productos.
- Sumar un filtro por rango de precio.
- Exportar el historial de ventas a un archivo CSV.
