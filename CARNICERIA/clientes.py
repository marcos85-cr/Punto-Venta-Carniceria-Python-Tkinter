######################################################################################################################
# Nombre del programa: PROYECTO CARNICERIA.PY
# Nombres del programador: [Marcos Vargas Hernández]
# Fecha de elaboración del programa: 14-04-2025
# Versión del Python: 3.13.2
# Nombre del IDE donde se desarrolló el programa: Visual Studio Code
######################################################################################################################
import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk # Importar la librería PIL para trabajar con imágenes

"""
Clase Clientes:
    Esta clase representa la ventana de gestión de clientes en la aplicación de carnicería.
    Hereda de tk.Frame para crear un marco que contendrá los widgets de la interfaz gráfica.
"""

class Clientes(tk.Frame): # Definición de la clase Clientes que hereda de tk.Frame
    db_name = "database.db"  # Declaración global

    def __init__(self, padre, update_callback=None):
        super().__init__(padre) 
        self.update_callback = update_callback  # Guardamos la función de actualización
        self.widgets() # Llamamos a la función widgets para crear los elementos de la ventana
        self.cargar_registros() # Cargar registros al iniciar la ventana

    def widgets(self):
        # Creación del frame que va albergar los labels
        self.labelframe = tk.LabelFrame(self, text="Clientes", font="sans 18 bold", bg="#477296", relief="raised", borderwidth=1)
        self.labelframe.place(x=20, y=20, width=250, height=560)

        # Creación del label Nombre
        lblnombre = tk.Label(self.labelframe, text="Nombre: ", font="sans 14 bold", bg="#477296")
        lblnombre.place(x=10, y=20)
        self.nombre = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.nombre.place(x=10, y=50, width=220, height=40)

        # Creación del label cédula
        lblcedula = tk.Label(self.labelframe, text="Cédula: ", font="sans 14 bold", bg="#477296")
        lblcedula.place(x=10, y=100)
        self.cedula = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.cedula.place(x=10, y=130, width=220, height=40)

        # Creación del teléfono
        lbltelefono = tk.Label(self.labelframe, text="Teléfono: ", font="sans 14 bold", bg="#477296")
        lbltelefono.place(x=10, y=180)
        self.telefono = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.telefono.place(x=10, y=210, width=220, height=40)

        # Creación del dirección
        lbldireccion = tk.Label(self.labelframe, text="Dirección: ", font="sans 14 bold", bg="#477296")
        lbldireccion.place(x=10, y=260)
        self.direccion = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.direccion.place(x=10, y=290, width=220, height=40)

        # Creación del correo eléctronico
        lblcorreo = tk.Label(self.labelframe, text="Correo: ", font="sans 14 bold", bg="#477296")
        lblcorreo.place(x=10, y=340)
        self.correo = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.correo.place(x=10, y=370, width=220, height=40)

        # imagen boton Agregar
        imagen_pil = Image.open("iconos/agregar.png")
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk_agregar = ImageTk.PhotoImage(imagen_resize)

        # imagen boton Editar
        imagen_pil = Image.open("iconos/editar.png")
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk_editar = ImageTk.PhotoImage(imagen_resize)

        #  Creación de los botones
        btn1 = Button(self.labelframe, fg="Black", text="Ingresar", font="sans 16 bold",
                      highlightthickness=0, relief="flat", borderwidth=0, command=self.registrar)
        btn1.config(image=imagen_tk_agregar, compound=LEFT, padx=15)
        btn1.image = imagen_tk_agregar
        btn1.place(x=10, y=420, width=220, height=40)

        btn2 = Button(self.labelframe, fg="Black", text="Modificar",
                      font="sans 16 bold", highlightthickness=0, relief="flat", borderwidth=0, command=self.modificar)
        btn2.config(image=imagen_tk_editar, compound=LEFT, padx=15)
        btn2.image = imagen_tk_editar
        btn2.place(x=10, y=470, width=220, height=40)

        # Creación del labelframe en blanco para los datos
        treFrame = Frame(self, bg="white", relief="raised", borderwidth=3)
        treFrame.place(x=280, y=32, width=850, height=550)

        # Utilizar barras de desplazamiento vertical
        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT, fill=Y)

        # Utilizar barras de desplazamiento horizontal
        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        self.tre = ttk.Treeview(treFrame, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, height=40,
                                columns=("ID", "Nombre", "Cédula", "Teléfono", "Dirección", "Correo"), show="headings") # Se crea la tabla

        self.tre.pack(expand=True, fill=BOTH) # Se expande la tabla para llenar el espacio disponible

        scrol_y.config(command=self.tre.yview) # Se configura la barra de desplazamiento vertical
        scrol_x.config(command=self.tre.xview) # Se configura la barra de desplazamiento horizontal
        # Se crean los encabezados de la tabla
        self.tre.heading("ID", text="ID")
        self.tre.heading("Nombre", text="Nombre")
        self.tre.heading("Cédula", text="Cédula")
        self.tre.heading("Teléfono", text="Teléfono")
        self.tre.heading("Dirección", text="Dirección")
        self.tre.heading("Correo", text="Correo")

        # Se crean las columnas de la tabla
        self.tre.column("ID", width=50, anchor="center")
        self.tre.column("Nombre", width=150, anchor="center")
        self.tre.column("Cédula", width=120, anchor="center")
        self.tre.column("Teléfono", width=120, anchor="center")
        self.tre.column("Dirección", width=200, anchor="center")
        self.tre.column("Correo", width=200, anchor="center")

    def validar_campos(self):  # Validar que el campo Nombre no esté vacío
        if not self.nombre.get().strip():  # Verifica que el campo no esté vacío o solo tenga espacios
            messagebox.showerror("Error", "El campo 'Nombre' es obligatorio.")
            return False
        return True

    def registrar(self): # Función para registrar un cliente
        if not self.validar_campos():  
            return

        nombre = self.nombre.get() # Obtener el nombre del cliente
        cedula = self.cedula.get()
        telefono = self.telefono.get()
        direccion = self.direccion.get()
        correo = self.correo.get()

        try:
            conn = sqlite3.connect(self.db_name)  # Conexión a base de datos
            cursor = conn.cursor() # Cursor para ejecutar comandos SQL
            cursor.execute(
                "INSERT INTO clientes (nombre, cedula, telefono, direccion, correo) VALUES (?, ?, ?, ?, ?)",
                (nombre, cedula, telefono, direccion, correo),
            )
            conn.commit() # Guardar cambios en la base de datos
            conn.close() # Cerrar conexión a la base de datos

            messagebox.showinfo("Éxito", "Cliente registrado correctamente")

            # Actualizar la tabla automáticamente
            self.limpiar_treview()
            self.limpiar_Campos()
            self.cargar_registros()

            # Llamar al callback para actualizar punto_venta
            if self.update_callback:
                self.update_callback()

            # Forzar actualización de la interfaz
            self.update_idletasks()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar el cliente: {e}")

        # Mostrar registros en la interfaz grafica que se tienen guardados en la base de datos

    def cargar_registros(Self): # Carga los registros de la base de datos
        try:
            conn = sqlite3.connect(Self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes") # Selecciona todos los registros de la tabla clientes
            rows = cursor.fetchall() # Obtiene todos los registros
            for row in rows:
                Self.tre.insert("", "end", values=row) # Inserta cada registro en el Treeview
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror(
                "Error", f"No se pudo cargar los registros: {e}")

    # Limpia la tabla cada vez que se ingresa in registro
    def limpiar_treview(self):
        for item in self.tre.get_children(): # Recorre todos los elementos de la tabla
            self.tre.delete(item)

    # Limpia los campos cada vez que se ingresa un nuevo registro
    def limpiar_Campos(self): #
        self.nombre.delete(0, END)
        self.cedula.delete(0, END)
        self.telefono.delete(0, END)
        self.direccion.delete(0, END)
        self.correo.delete(0, END)

    def modificar(self):  # selección de clientes para modificar
        if not self.tre.selection():
            messagebox.showerror(
                "Error", "Por favor seleccione un cliente para modificar.")
            return

        item = self.tre.selection()[0] # Obtener el elemento seleccionado
        id_cliente = self.tre.item(item, "values")[0] # Obtener el ID del cliente seleccionado
        nombre_actual = self.tre.item(item, "values")[1] # Obtener el nombre del cliente seleccionado
        cedula_actual = self.tre.item(item, "values")[2]
        telefono_actual = self.tre.item(item, "values")[3]
        direccion_actual = self.tre.item(item, "values")[4]
        correo_actual = self.tre.item(item, "values")[5]

        # La ventana que se modifica se posiciona sobre las demas ventanas
        top_modificar = Toplevel(self)
        top_modificar.title("Modificar cliente")
        top_modificar.geometry("400x400+400+50")
        top_modificar.config(bg="#477296")
        top_modificar.resizable(False, False)
        top_modificar.transient(self.master)
        top_modificar.grab_set()
        top_modificar.focus_set()
        top_modificar.lift()

        # Creación de los labels y campos de texto para modificar
        tk.Label(top_modificar, text="Nombre: ", font="sans 14 bold", bg="#477296").grid(row=0, column=0, padx=10, pady=5) #
        nombre_nuevo = tk.Entry(top_modificar, font="sans 14 bold")
        nombre_nuevo.insert(0, nombre_actual)
        nombre_nuevo.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(top_modificar, text="Cédula: ", font="sans 14 bold", bg="#477296").grid(row=1, column=0, padx=10, pady=5)
        cedula_nuevo = tk.Entry(top_modificar, font="sans 14 bold")
        cedula_nuevo.insert(0, cedula_actual)
        cedula_nuevo.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(top_modificar, text="Teléfono: ", font="sans 14 bold", bg="#477296").grid(row=2, column=0, padx=10, pady=5)
        telefono_nuevo = tk.Entry(top_modificar, font="sans 14 bold")
        telefono_nuevo.insert(0, telefono_actual)
        telefono_nuevo.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(top_modificar, text="Dirección: ", font="sans 14 bold", bg="#477296").grid(row=3, column=0, padx=10, pady=5)
        direccion_nuevo = tk.Entry(top_modificar, font="sans 14 bold")
        direccion_nuevo.insert(0, direccion_actual)
        direccion_nuevo.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(top_modificar, text="Correo: ", font="sans 14 bold", bg="#477296").grid(row=4, column=0, padx=10, pady=5)
        correo_nuevo = tk.Entry(top_modificar, font="sans 14 bold")
        correo_nuevo.insert(0, correo_actual)
        correo_nuevo.grid(row=4, column=1, padx=10, pady=5)

        def guardar_modificaciones(): # Guardar los cambios realizados
            nuevo_nombre = nombre_nuevo.get() # Obtiene los datos de cada uno
            nueva_cedula = cedula_nuevo.get()
            nuevo_telefono = telefono_nuevo.get()
            nueva_direccion = direccion_nuevo.get()
            nuevo_correo = correo_nuevo.get()

            try:
                conn = sqlite3.connect(self.db_name)
                cursor = conn.cursor()
                cursor.execute(""" UPDATE clientes SET nombre = ?, cedula = ?, telefono = ?, direccion = ?, correo = ? WHERE id = ?""",
                               (nuevo_nombre, nueva_cedula, nuevo_telefono, nueva_direccion, nuevo_correo, id_cliente))
                conn.commit() # Guardar cambios en la base de datos
                conn.close() # Cerrar conexión a la base de datos
                messagebox.showinfo(
                    "Exito", "Cliente modificado correctamente")
                self.limpiar_treview()
                self.cargar_registros() # Cargar registros nuevamente
                top_modificar.destroy() # Cerrar la ventana de modificación
            except sqlite3.Error as e:
                messagebox.showerror(
                    "Error", f"No se pudo modificar el cliente: {e}")

        # Botón para guardar los cambios realizados
        btn_guardar = tk.Button(top_modificar, text="Guardar Cambios",
                                command=guardar_modificaciones, font="sans 14 bold", relief="raised", borderwidth=3)
        btn_guardar.grid(row=5, column=0, columnspan=2, pady=20)
