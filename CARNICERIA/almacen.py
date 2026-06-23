######################################################################################################################
# Nombre del programa: PROYECTO CARNICERIA.PY
# Nombres del programador: [Marcos Vargas Hernández]
# Fecha de elaboración del programa: 14-04-2025
# Versión del Python: 3.13.2
# Nombre del IDE donde se desarrolló el programa: Visual Studio Code
######################################################################################################################

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class Almacen(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.config(bg="#1F2937")
        self.create_widgets()
        self.mostrar_datos()

    def conectar_db(self):
        return sqlite3.connect("database.db")

    def obtener_almacenes(self):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT almacen FROM articulos")
            almacenes = [row[0] for row in cursor.fetchall()]
            conn.close()
            return almacenes
        except Exception as e:
            print("Error al obtener almacenes:", e)
            return []

    def create_widgets(self):
        top_frame = tk.Frame(self, bg="#477296")
        top_frame.pack(pady=10, padx=10, fill="x")

        btn_nuevo = tk.Button(top_frame, text="Registrar Producto", bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296", command=self.abrir_ventana_registro)
        btn_nuevo.pack(side="left", padx=5)

        btn_eliminar = tk.Button(top_frame, text="Eliminar Producto", bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296", command=self.eliminar_producto)
        btn_eliminar.pack(side="left", padx=5)

        tk.Label(top_frame, text="Traspasar artículo:", bg="#477296", fg="white").pack(side="left", padx=5)
        self.combo_articulos = ttk.Combobox(top_frame, width=30)
        self.combo_articulos.pack(side="left", padx=5)

        self.combo_destino = ttk.Combobox(top_frame, values=self.obtener_almacenes(), width=25)
        self.combo_destino.pack(side="left", padx=5)

        btn_traspasar = tk.Button(top_frame, text="Traspasar", bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296", command=self.traspasar_producto)
        btn_traspasar.pack(side="left", padx=5)

        # CAMBIO AQUÍ: Se elimina expand=True
        table_frame = tk.Frame(self)
        table_frame.pack(padx=10, pady=10, fill="x", expand=False)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Artículo", "Stock", "Estado", "Almacén"),
            show="headings",
            height=12  # ← Define cantidad de filas visibles
        )

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#111827", foreground="white", fieldbackground="#111827", rowheight=25)
        style.configure("Treeview.Heading", background="#374151", foreground="white", font=('Segoe UI', 10, 'bold'))
        style.map("Treeview", background=[('selected', '#2563EB')])

        self.tree.heading("ID", text="ID")
        self.tree.column("ID", anchor="center", width=50, stretch=False)

        self.tree.heading("Artículo", text="Artículo")
        self.tree.column("Artículo", anchor="w", width=250)

        self.tree.heading("Stock", text="Stock")
        self.tree.column("Stock", anchor="center", width=80)

        self.tree.heading("Estado", text="Estado")
        self.tree.column("Estado", anchor="center", width=100)

        self.tree.heading("Almacén", text="Almacén")
        self.tree.column("Almacén", anchor="center", width=180)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")

        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=hsb.set)
        hsb.pack(side="bottom", fill="x")

        # CAMBIO AQUÍ: ya no se usa expand
        self.tree.pack(fill="both", expand=False)




    def mostrar_datos(self):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id, articulos, stock, estado, almacen FROM articulos")
            rows = cursor.fetchall()

            self.tree.delete(*self.tree.get_children())

            for row in rows:
                self.tree.insert("", "end", values=row)

            conn.close()

            self.combo_articulos["values"] = [f"{row[0]} - {row[1]}" for row in rows]
            self.combo_destino["values"] = self.obtener_almacenes()
        except Exception as e:
            print("Error al mostrar datos:", e)

    def abrir_ventana_registro(self):
        popup = tk.Toplevel(self)
        popup.title("Registrar Producto")
        popup.configure(bg="#477296")
        popup.geometry("400x300")
        popup.resizable(False, False)

        tk.Label(popup, text="Artículo:", bg="#477296", fg="white", font="sans 16").pack(pady=5)
        entry_articulo = tk.Entry(popup, bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        entry_articulo.pack()

        tk.Label(popup, text="Stock:", bg="#477296", fg="white", font="sans 16").pack(pady=5)
        entry_stock = tk.Entry(popup, bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        entry_stock.pack()

        tk.Label(popup, text="Estado:", bg="#477296", fg="white", font="sans 16").pack(pady=5)
        combo_estado = ttk.Combobox(popup, values=["Activo", "Inactivo"])
        combo_estado.pack()

        tk.Label(popup, text="Almacén:", bg="#477296", fg="white", font="sans 16").pack(pady=5)
        combo_almacen = ttk.Combobox(popup, values=self.obtener_almacenes())
        combo_almacen.pack()

        def guardar():
            articulo = entry_articulo.get()
            stock = entry_stock.get()
            estado = combo_estado.get()
            almacen = combo_almacen.get()

            if not articulo or not stock or not estado or not almacen:
                messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios")
                return

            try:
                conn = self.conectar_db()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO articulos (articulos, stock, estado, almacen) VALUES (?, ?, ?, ?)",
                               (articulo, stock, estado, almacen))
                conn.commit()
                conn.close()

                self.mostrar_datos()

                entry_articulo.delete(0, tk.END)
                entry_stock.delete(0, tk.END)
                combo_estado.set("")
                combo_almacen.set("")

                messagebox.showinfo("Éxito", "Producto registrado correctamente")
            except Exception as e:
                print("Error al registrar producto:", e)
                messagebox.showerror("Error", "No se pudo registrar el producto")

        tk.Button(popup, text="Guardar",bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296" ,command=guardar).pack(pady=10)

    def traspasar_producto(self):
        seleccionado = self.combo_articulos.get()
        destino = self.combo_destino.get()

        if not seleccionado or not destino:
            messagebox.showwarning("Campos vacíos", "Seleccione un artículo y almacén de destino")
            return

        try:
            id_articulo = int(seleccionado.split(" - ")[0])
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE articulos SET almacen = ? WHERE id = ?", (destino, id_articulo))
            conn.commit()
            conn.close()

            self.mostrar_datos()
            messagebox.showinfo("Éxito", "Artículo traspasado correctamente")
        except Exception as e:
            print("Error al traspasar producto:", e)
            messagebox.showerror("Error", "No se pudo traspasar el artículo")

    def eliminar_producto(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Sin selección", "Seleccione un producto de la tabla para eliminar.")
            return

        valores = self.tree.item(selected_item, 'values')
        producto_id = valores[0]

        confirmar = messagebox.askyesno("Confirmar eliminación", f"¿Está seguro que desea eliminar el producto ID {producto_id}?")
        if not confirmar:
            return

        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM articulos WHERE id = ?", (producto_id,))
            conn.commit()
            conn.close()

            self.mostrar_datos()
            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
        except Exception as e:
            print("Error al eliminar producto:", e)
            messagebox.showerror("Error", "No se pudo eliminar el producto.")
