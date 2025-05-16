######################################################################################################################
# Nombre del programa:PROYECTO CARNICERIA.PY
# Número del grupo de trabajo: 2 - Snake Coders
# Nombres de los programadores:
# Daniel Cordero Porras
# Marcos Vargas Hernandez
# Angelo Bermudez Ayales
# Fecha de elaboración del programa: 14-04-2025
# Versión del Python: 3.13.2
# Nombre del IDE donde se desarrollo el programa: Visual Studio Code
######################################################################################################################

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Clase principal del módulo de Inventario, hereda de tk.Frame
class Inventario(tk.Frame):
    def __init__(self, master=None):
        # Inicialización del Frame
        super().__init__(master, bg="#477296")
        self.pack(fill="both", expand=True)
        self.conectar_bd()         # Conexión a la base de datos
        self.crear_widgets()       # Creación de la interfaz
        self.mostrar_productos()   # Cargar datos en la tabla

    def conectar_bd(self):
        # Método para conectar a la base de datos SQLite
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()

    def crear_widgets(self):
        # Crear todos los widgets de la interfaz

        # Título del módulo
        titulo = tk.Label(self, text="Inventario de Productos", font=("Arial", 18, "bold"), bg="#477296", fg="white")
        titulo.pack(pady=10)

        # Frame principal que contiene el formulario y la tabla
        main_frame = tk.Frame(self, bg="#477296")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ---------- Sección izquierda: formulario de entrada ----------
        form_frame = tk.Frame(main_frame, bg="#477296")
        form_frame.pack(side="left", padx=10, pady=10, anchor="n")

        # Lista de campos de entrada
        labels = ["ID", "Nombre", "Precio", "Costo", "Stock", "Estado"]
        self.entries = {}  # Diccionario para guardar las entradas

        # Crear etiquetas y entradas para cada campo
        for i, label in enumerate(labels):
            tk.Label(
                form_frame,
                text=label + ":",
                bg="#477296",
                fg="white",
                font="sans 12 bold"
            ).grid(row=i, column=0, sticky="w", pady=6)

            entry = tk.Entry(
                form_frame,
                bg="white",
                fg="black",
                font="sans 12 bold",
                width=15,
                borderwidth=0,
                highlightthickness=0,
                relief="flat"
            )
            entry.grid(row=i, column=1, pady=6, ipady=6, sticky="w")
            self.entries[label.lower()] = entry

        # ---------- Botones del formulario ----------
        button_frame = tk.Frame(form_frame, bg="#477296")
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)

        # Definición de botones y sus funciones
        botones = [
            ("Buscar", self.buscar_producto),
            ("Actualizar", self.actualizar_producto),
            ("Eliminar", self.eliminar_producto),
            ("Limpiar Campos", self.limpiar_campos)
        ]

        # Crear botones
        for i, (texto, comando) in enumerate(botones):
            b = tk.Button(button_frame, text=texto, width=18, height=1, command=comando, bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
            b.grid(row=i, column=0, pady=4, padx=5)

        # ---------- Sección derecha: tabla de productos ----------
        tabla_frame = tk.Frame(main_frame, bg="#477296")
        tabla_frame.pack(side="left", fill="both", expand=True, padx=10)

        # Estilo de la tabla (Treeview)
        style = ttk.Style()
        style.configure("Treeview", rowheight=28, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

        columnas = ("ID", "Artículo", "Precio", "Costo", "Stock", "Estado")
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings")
        self.tabla.configure(selectmode="browse")

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.pack(fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Ancho de columnas
        anchos_columnas = {
            "ID": 50,
            "Artículo": 200,
            "Precio": 100,
            "Costo": 100,
            "Stock": 80,
            "Estado": 100
        }

        # Configurar columnas de la tabla
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center", width=anchos_columnas[col])

        # Línea final decorativa
        linea_final = tk.Frame(tabla_frame, height=2, bg="#477296")
        linea_final.pack(fill="x", side="bottom")

        # Vincular selección de fila con función
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    def mostrar_productos(self):
        # Mostrar todos los productos de la base de datos en la tabla
        self.tabla.delete(*self.tabla.get_children())
        self.cursor.execute("SELECT id, articulos, precio, costo, stock, estado FROM articulos")
        for producto in self.cursor.fetchall():
            self.tabla.insert("", tk.END, values=producto)

    def buscar_producto(self):
        # Buscar producto por ID o por nombre
        id_valor = self.entries["id"].get().strip()
        nombre_valor = self.entries["nombre"].get().strip()
        self.tabla.delete(*self.tabla.get_children())

        if id_valor:
            self.cursor.execute("SELECT * FROM articulos WHERE id = ?", (id_valor,))
        elif nombre_valor:
            self.cursor.execute("SELECT * FROM articulos WHERE articulos LIKE ?", ('%' + nombre_valor + '%',))
        else:
            messagebox.showwarning("Entrada requerida", "Debe ingresar un ID o Nombre para buscar.")
            return

        productos = self.cursor.fetchall()
        if productos:
            for producto in productos:
                self.tabla.insert("", tk.END, values=producto)
                self.llenar_campos(producto)
        else:
            messagebox.showinfo("No encontrado", "No se encontró el producto.")

    def llenar_campos(self, producto):
        # Cargar los datos del producto en los campos de entrada
        campos = ["id", "nombre", "precio", "costo", "stock", "estado"]
        for i, campo in enumerate(campos):
            self.entries[campo].delete(0, tk.END)
            self.entries[campo].insert(0, producto[i])

    def seleccionar_fila(self, event):
        # Al seleccionar una fila en la tabla, llenar los campos del formulario
        item_seleccionado = self.tabla.focus()
        if not item_seleccionado:
            return
        valores = self.tabla.item(item_seleccionado)["values"]
        if valores:
            campos = ["id", "nombre", "precio", "costo", "stock", "estado"]
            for i, campo in enumerate(campos):
                self.entries[campo].delete(0, tk.END)
                self.entries[campo].insert(0, valores[i])

    def actualizar_producto(self):
        # Agregar o actualizar un producto según si ya existe en la base de datos
        try:
            producto_id = self.entries["id"].get().strip()

            if not producto_id:
                messagebox.showwarning("Campo faltante", "Debe ingresar el ID del producto para actualizar.")
                return

            self.cursor.execute("SELECT * FROM articulos WHERE id=?", (producto_id,))
            existe = self.cursor.fetchone()

            datos = (
                self.entries["nombre"].get(),
                float(self.entries["precio"].get()),
                float(self.entries["costo"].get()),
                float(self.entries["stock"].get()),
                self.entries["estado"].get()
            )

            if existe:
                self.cursor.execute(
                    "UPDATE articulos SET articulos=?, precio=?, costo=?, stock=?, estado=? WHERE id=?",
                    datos + (producto_id,)
                )
                mensaje = "Producto actualizado correctamente."
            else:
                self.cursor.execute(
                    "INSERT INTO articulos (id, articulos, precio, costo, stock, estado) VALUES (?, ?, ?, ?, ?, ?)",
                    (producto_id,) + datos
                )
                mensaje = "Producto agregado correctamente."

            self.conn.commit()
            messagebox.showinfo("Éxito", mensaje)
            self.mostrar_productos()
            self.limpiar_campos()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el producto: {e}")

    def editar_producto(self):
        # Actualizar un producto existente (versión alternativa)
        try:
            datos = (
                self.entries["nombre"].get(),
                float(self.entries["precio"].get()),
                float(self.entries["costo"].get()),
                float(self.entries["stock"].get()),
                self.entries["estado"].get(),
                int(self.entries["id"].get())
            )
            self.cursor.execute(
                "UPDATE articulos SET articulos=?, precio=?, costo=?, stock=?, estado=? WHERE id=?", datos
            )
            self.conn.commit()
            messagebox.showinfo("Éxito", "Producto actualizado.")
            self.mostrar_productos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar: {e}")

    def eliminar_producto(self):
        # Eliminar un producto de la base de datos por su ID
        try:
            producto_id = int(self.entries["id"].get())
            self.cursor.execute("DELETE FROM articulos WHERE id=?", (producto_id,))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Producto eliminado.")
            self.mostrar_productos()
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    def limpiar_campos(self):
        # Limpiar todos los campos del formulario
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.mostrar_productos()
