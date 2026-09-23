"""
gui.py
Interfaz gráfica de la aplicación de kiosco, hecha con Tkinter.
Conecta la base de datos (database.py), la lógica de negocio (logic.py)
y las estructuras de datos (estructuras.py).
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from src import database
from src import logic
from src.estructuras import Pila, busqueda_binaria_recursiva


class AppKiosco(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Kiosco")
        self.geometry("800x560")

        database.crear_tabla()

        # Pila (TDA) con el historial de ventas
        self.historial_ventas = Pila()
        self._cargar_historial_desde_db()

        self._crear_widgets()
        self.refrescar_tabla()

    # ---------- Construcción de la interfaz ----------

    def _crear_widgets(self):
        # --- Formulario de carga / edición ---
        frame_form = tk.LabelFrame(self, text="Producto")
        frame_form.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_form, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre = tk.Entry(frame_form)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Precio:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_precio = tk.Entry(frame_form)
        self.entry_precio.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_form, text="Stock:").grid(row=0, column=4, padx=5, pady=5)
        self.entry_stock = tk.Entry(frame_form)
        self.entry_stock.grid(row=0, column=5, padx=5, pady=5)

        tk.Button(frame_form, text="Agregar", command=self.agregar).grid(
            row=1, column=1, pady=5
        )
        tk.Button(
            frame_form, text="Modificar seleccionado", command=self.modificar
        ).grid(row=1, column=2, columnspan=2, pady=5)
        tk.Button(
            frame_form, text="Eliminar seleccionado", command=self.eliminar
        ).grid(row=1, column=4, columnspan=2, pady=5)

        # --- Búsqueda, orden y filtro ---
        frame_acciones = tk.LabelFrame(self, text="Buscar / Ordenar / Filtrar")
        frame_acciones.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_acciones, text="Buscar por nombre exacto:").grid(
            row=0, column=0, padx=5, pady=5
        )
        self.entry_busqueda = tk.Entry(frame_acciones)
        self.entry_busqueda.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(frame_acciones, text="Buscar", command=self.buscar).grid(
            row=0, column=2, padx=5
        )

        tk.Button(
            frame_acciones, text="Ordenar por precio", command=self.ordenar_precio
        ).grid(row=0, column=3, padx=5)
        tk.Button(
            frame_acciones, text="Filtrar stock bajo (≤5)", command=self.filtrar_stock
        ).grid(row=0, column=4, padx=5)
        tk.Button(
            frame_acciones, text="Mostrar todos", command=self.refrescar_tabla
        ).grid(row=0, column=5, padx=5)

        # --- Tabla de productos ---
        self.tabla = ttk.Treeview(
            self, columns=("id", "nombre", "precio", "stock"), show="headings", height=10
        )
        for col, titulo in zip(
            ("id", "nombre", "precio", "stock"), ("ID", "Nombre", "Precio", "Stock")
        ):
            self.tabla.heading(col, text=titulo)
            self.tabla.column(col, width=130)
        self.tabla.pack(fill="both", expand=True, padx=10, pady=5)

        # --- Ventas ---
        frame_ventas = tk.LabelFrame(self, text="Venta")
        frame_ventas.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_ventas, text="Cantidad a vender:").grid(
            row=0, column=0, padx=5, pady=5
        )
        self.entry_cantidad_venta = tk.Entry(frame_ventas, width=6)
        self.entry_cantidad_venta.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(
            frame_ventas, text="Vender producto seleccionado", command=self.vender
        ).grid(row=0, column=2, padx=5)
        tk.Button(
            frame_ventas, text="Ver historial de ventas", command=self.ver_historial
        ).grid(row=0, column=3, padx=5)

    def _cargar_historial_desde_db(self):
        """Reconstruye la Pila de historial a partir de lo guardado en la base de datos."""
        for id_venta, nombre, cantidad, total, fecha in database.consultar_ventas():
            self.historial_ventas.apilar(
                {"producto": nombre, "cantidad": cantidad, "total": total, "fecha": fecha}
            )

    # ---------- Utilidades internas ----------

    def _obtener_seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccioná un producto de la tabla primero.")
            return None
        return self.tabla.item(seleccion[0])["values"]

    def _mostrar_lista(self, productos):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        for producto in productos:
            self.tabla.insert("", tk.END, values=producto)

    def refrescar_tabla(self):
        self._mostrar_lista(database.consultar_todos())

    def _limpiar_formulario(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)

    # ---------- Acciones CRUD ----------

    def agregar(self):
        valido, precio_o_error, stock = logic.validar_producto(
            self.entry_nombre.get(), self.entry_precio.get(), self.entry_stock.get()
        )
        if not valido:
            messagebox.showerror("Datos inválidos", precio_o_error)
            return

        database.alta_producto(self.entry_nombre.get().strip(), precio_o_error, stock)
        self._limpiar_formulario()
        self.refrescar_tabla()

    def modificar(self):
        seleccionado = self._obtener_seleccionado()
        if not seleccionado:
            return
        id_producto = seleccionado[0]

        nombre = self.entry_nombre.get().strip() or seleccionado[1]
        precio_texto = self.entry_precio.get() or str(seleccionado[2])
        stock_texto = self.entry_stock.get() or str(seleccionado[3])

        valido, precio_o_error, stock = logic.validar_producto(
            nombre, precio_texto, stock_texto
        )
        if not valido:
            messagebox.showerror("Datos inválidos", precio_o_error)
            return

        database.modificar_producto(id_producto, nombre, precio_o_error, stock)
        self._limpiar_formulario()
        self.refrescar_tabla()

    def eliminar(self):
        seleccionado = self._obtener_seleccionado()
        if not seleccionado:
            return
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{seleccionado[1]}'?"):
            database.eliminar_producto(seleccionado[0])
            self.refrescar_tabla()

    # ---------- Búsqueda, orden y filtro ----------

    def buscar(self):
        nombre_buscado = self.entry_busqueda.get().strip()
        if not nombre_buscado:
            messagebox.showwarning("Atención", "Escribí un nombre para buscar.")
            return

        productos_ordenados = logic.ordenar_por_nombre(database.consultar_todos())
        resultado = busqueda_binaria_recursiva(productos_ordenados, nombre_buscado)

        if resultado is None:
            messagebox.showinfo(
                "Sin resultados", "No se encontró ningún producto con ese nombre."
            )
            self._mostrar_lista([])
        else:
            self._mostrar_lista([resultado])

    def ordenar_precio(self):
        self._mostrar_lista(logic.ordenar_por_precio(database.consultar_todos()))

    def filtrar_stock(self):
        self._mostrar_lista(logic.filtrar_stock_bajo(database.consultar_todos(), limite=5))

    # ---------- Ventas (usa la Pila) ----------

    def vender(self):
        seleccionado = self._obtener_seleccionado()
        if not seleccionado:
            return

        try:
            cantidad = int(self.entry_cantidad_venta.get())
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero.")
            return

        # Conversión explícita: los valores que vuelven de la tabla a veces
        # llegan como texto, y comparar texto con número rompe el programa
        # sin avisar. Convertimos todo a su tipo correcto antes de usarlo.
        try:
            id_producto = int(seleccionado[0])
            nombre = str(seleccionado[1])
            precio = float(seleccionado[2])
            stock_actual = int(seleccionado[3])
        except (ValueError, IndexError):
            messagebox.showerror("Error", "No se pudo leer el producto seleccionado.")
            return

        if cantidad <= 0:
            messagebox.showerror("Error", "La cantidad debe ser mayor a 0.")
            return
        if cantidad > stock_actual:
            messagebox.showerror("Error", "No hay stock suficiente.")
            return

        total = cantidad * precio
        nuevo_stock = stock_actual - cantidad

        try:
            database.actualizar_stock(id_producto, nuevo_stock)
            fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
            database.registrar_venta(id_producto, cantidad, total, fecha)
        except Exception as error:
            messagebox.showerror("Error al guardar la venta", str(error))
            return

        # Apilamos la venta en el historial (TDA Pila)
        self.historial_ventas.apilar(
            {"producto": nombre, "cantidad": cantidad, "total": total, "fecha": fecha}
        )

        messagebox.showinfo(
            "Venta registrada", f"Vendiste {cantidad} de '{nombre}' por ${total:.2f}"
        )
        self.entry_cantidad_venta.delete(0, tk.END)
        self.refrescar_tabla()

    def ver_historial(self):
        ventana = tk.Toplevel(self)
        ventana.title("Historial de ventas (más reciente primero)")
        ventana.geometry("420x300")

        texto = tk.Text(ventana)
        texto.pack(fill="both", expand=True)

        ventas = self.historial_ventas.como_lista()
        if not ventas:
            texto.insert(tk.END, "Todavía no se registraron ventas en esta sesión.")
        else:
            for venta in ventas:
                texto.insert(
                    tk.END,
                    f"{venta['fecha']} - {venta['producto']} x{venta['cantidad']} "
                    f"= ${venta['total']:.2f}\n",
                )
        texto.config(state="disabled")
