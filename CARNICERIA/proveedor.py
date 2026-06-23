######################################################################################################################
# Nombre del programa: PROYECTO CARNICERIA.PY
# Nombres del programador: [Marcos Vargas Hernández]
# Fecha de elaboración del programa: 14-04-2025
# Versión del Python: 3.13.2
# Nombre del IDE donde se desarrolló el programa: Visual Studio Code
######################################################################################################################
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk

"""
Clase Proveedor:
    Esta clase representa el formulario para registrar proveedores en la base de datos.
    Hereda de tk.Frame y contiene métodos para crear widgets, validar campos, guardar proveedores y cargar registros.
"""

class Proveedor(tk.Frame):  # Hereda de tk.Frame
    db_name = "database.db"

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # Guarda la referencia al padre
        self.widgets()  # Llama a la función para crear los widgets
        self.cargar_registros() # Carga los registros al iniciar la ventana

    def limpiar_treeview(self): # Limpia el Treeview
        for item in self.tree.get_children(): # Itera sobre los elementos del Treeview
            self.tree.delete(item) # Elimina cada elemento

    def limpiar_campos(self): # Limpia los campos de entrada
        # Limpia los campos de entrada de texto
        self.entry_nombre.delete(0, tk.END) # Elimina el texto del campo de nombre
        self.entry_cedula.delete(0, tk.END) # Elimina el texto del campo de cédula
        self.entry_direccion.delete(0, tk.END) # Elimina el texto del campo de dirección
        self.entry_telefono.delete(0, tk.END) # Elimina el texto del campo de teléfono
        self.entry_correo.delete(0, tk.END) # Elimina el texto del campo de correo electrónico
        self.entry_cuenta.delete(0, tk.END) # Elimina el texto del campo de cuenta bancaria

    def validar_campos(self): # Valida que todos los campos estén llenos
        return all([
            self.entry_nombre.get(), # Verifica que Ccada campo no este vacio
            self.entry_cedula.get(), 
            self.entry_direccion.get(),
            self.entry_telefono.get(),
            self.entry_correo.get(),
            self.entry_cuenta.get()
        ])

    def guardar_proveedor(self): # Guarda el proveedor en la base de datos
        if not self.validar_campos(): # Verifica que todos los campos estén llenos
            messagebox.showwarning("Advertencia", "Todos los campos deben estar llenos") # Muestra un mensaje de advertencia
            return

        nombre = self.entry_nombre.get() # Obtiene el nombre del proveedor
        cedula = self.entry_cedula.get() # Obtiene la cédula del proveedor
        direccion = self.entry_direccion.get()  # Obtiene la dirección del proveedor
        telefono = self.entry_telefono.get() # Obtiene el teléfono del proveedor
        correo = self.entry_correo.get()    # Obtiene el correo electrónico del proveedor
        cuenta = self.entry_cuenta.get() # Obtiene la cuenta bancaria del proveedor

        try:
            conn = sqlite3.connect(self.db_name) # Conecta a la base de datos
            cursor = conn.cursor() # Crea un cursor para ejecutar comandos SQL
            cursor.execute("INSERT INTO proveedor (nombre, cedula, direccion, telefono, correo, cuenta) VALUES (?, ?, ?, ?, ?, ?)", 
                           (nombre, cedula, direccion, telefono, correo, cuenta)) # Inserta el proveedor en la base de datos
            conn.commit() # Guarda los cambios en la base de datos
            messagebox.showinfo("Éxito", "Proveedor registrado con éxito")
        except sqlite3.Error as e:
            messagebox.showerror(
                "Error", f"Error al guardar el proveedor: {e}") # Muestra un mensaje de error si ocurre un problema al guardar el proveedor
        finally:
            conn.close() # Cierra la conexión a la base de datos

        self.limpiar_treeview() # Limpia el Treeview
        self.limpiar_campos() # Limpia los campos de entrada
        self.cargar_registros() # Carga los registros nuevamente para mostrar el nuevo proveedor

    def cargar_registros(self): # Carga los registros de la base de datos
        try:
            conn = sqlite3.connect(self.db_name) # Conecta a la base de datos
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM proveedor") # Selecciona todos los registros de la tabla proveedor
            registros = cursor.fetchall() # Obtiene todos los registros
            self.limpiar_treeview() # Limpia el Treeview antes de cargar nuevos registros
            for registro in registros:
                self.tree.insert("", tk.END, values=registro) # Inserta cada registro en el Treeview
            conn.close() # Cierra la conexión a la base de datos
        except sqlite3.Error as e:
            messagebox.showerror(
                "Error", f"Error al cargar los registros: {e}") # Muestra un mensaje de error si ocurre un problema al cargar los registros

    def editar_proveedor(self):  # Edita el proveedor seleccionado en el Treeview
        selected_item = self.tree.selection()  # Obtiene el elemento seleccionado en el Treeview
        if not selected_item:  # Verifica si hay un elemento seleccionado
            messagebox.showwarning("Advertencia", "Seleccione un proveedor para editar")  # Muestra un mensaje de advertencia si no hay un elemento seleccionado
            return
        item = self.tree.item(selected_item)  # Obtiene el elemento seleccionado
        values = item["values"]  # Obtiene los valores del elemento seleccionado

        # Validar que los valores tengan la longitud esperada
        if len(values) < 6:
            messagebox.showerror("Error", "El registro seleccionado no tiene todos los campos necesarios.")
            return

        self.entry_nombre.delete(0, tk.END)  # Limpia el campo de nombre
        self.entry_nombre.insert(0, values[0])  # Inserta el nombre del proveedor en el campo de nombre

        self.entry_cedula.delete(0, tk.END)  # Limpia el campo de cédula
        self.entry_cedula.insert(0, values[1])  # Inserta la cédula del proveedor en el campo de cédula

        self.entry_direccion.delete(0, tk.END)  # Limpia el campo de dirección
        self.entry_direccion.insert(0, values[2])  # Inserta la dirección del proveedor en el campo de dirección

        self.entry_telefono.delete(0, tk.END)  # Limpia el campo de teléfono
        self.entry_telefono.insert(0, values[3])  # Inserta el teléfono del proveedor en el campo de teléfono

        self.entry_correo.delete(0, tk.END)  # Limpia el campo de correo electrónico
        self.entry_correo.insert(0, values[4])  # Inserta el correo electrónico del proveedor en el campo de correo electrónico

        self.entry_cuenta.delete(0, tk.END)  # Limpia el campo de cuenta bancaria
        self.entry_cuenta.insert(0, values[5])  # Inserta la cuenta bancaria del proveedor en el campo de cuenta bancaria
    
    def guardar_edicion(self):  # Guarda la edición del proveedor
        """ Guarda los cambios realizados en el proveedor seleccionado """

        selected_item = self.tree.selection()  # Obtiene el elemento seleccionado en el Treeview
        if not selected_item:  # Verifica si hay un elemento seleccionado
            messagebox.showwarning("Advertencia", "Seleccione un proveedor para guardar los cambios")  # Muestra un mensaje de advertencia si no hay un elemento seleccionado
            return

        item = self.tree.item(selected_item)  # Obtiene el elemento seleccionado
        values = item["values"]  # Obtiene los valores del elemento seleccionado

        # Validar que los valores tengan la longitud esperada
        if len(values) < 6:
            messagebox.showerror("Error", "El registro seleccionado no tiene todos los campos necesarios.")
            return

        # Obtener los datos editados de los campos de entrada
        nombre = self.entry_nombre.get()
        cedula = self.entry_cedula.get()
        direccion = self.entry_direccion.get()
        telefono = self.entry_telefono.get()
        correo = self.entry_correo.get()
        cuenta = self.entry_cuenta.get()

        try: 
            conn = sqlite3.connect(self.db_name)  # Conecta a la base de datos
            cursor = conn.cursor()  # Crea un cursor para ejecutar comandos SQL

            # Actualiza el registro en la base de datos usando la cédula como identificador único
            cursor.execute("""
                UPDATE proveedor
                SET nombre = ?, direccion = ?, telefono = ?, correo = ?, cuenta = ? 
                WHERE cedula = ?
            """, (nombre, direccion, telefono, correo, cuenta, cedula))

            conn.commit()  # Guarda los cambios en la base de datos
            messagebox.showinfo("Éxito", "Proveedor actualizado con éxito")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al guardar los cambios: {e}")  # Muestra un mensaje de error si ocurre un problema
        finally:
            conn.close()  # Cierra la conexión a la base de datos

        self.limpiar_treeview()  # Limpia el Treeview
        self.limpiar_campos()  # Limpia los campos de entrada
        self.cargar_registros()  # Carga los registros nuevamente para reflejar los cambios
        

    def eliminar_proveedor(self):  # Elimina el proveedor seleccionado en el Treeview
        """ Elimina el proveedor seleccionado en el Treeview """

        selected_item = self.tree.selection()  # Obtiene el elemento seleccionado en el Treeview
        if not selected_item:  # Verifica si hay un elemento seleccionado
            messagebox.showwarning("Advertencia", "Seleccione un proveedor para eliminar")  # Muestra un mensaje de advertencia si no hay un elemento seleccionado
            return

        item = self.tree.item(selected_item)  # Obtiene el elemento seleccionado
        values = item["values"]  # Obtiene los valores del elemento seleccionado

        # Validar que los valores tengan la longitud esperada
        if len(values) < 6:
            messagebox.showerror("Error", "El registro seleccionado no tiene todos los campos necesarios.")
            return

        cedula = values[1]  # Obtiene la cédula del proveedor (identificador único)

        # Confirmación antes de eliminar
        confirmacion = messagebox.askyesno("Confirmación", f"¿Está seguro de que desea eliminar al proveedor con cédula {cedula}?")
        if not confirmacion:
            return

        try:
            conn = sqlite3.connect(self.db_name)  # Conecta a la base de datos
            cursor = conn.cursor()  # Crea un cursor para ejecutar comandos SQL

            # Elimina el registro de la base de datos usando la cédula como identificador único
            cursor.execute("DELETE FROM proveedor WHERE cedula = ?", (cedula,))
            conn.commit()  # Guarda los cambios en la base de datos

            messagebox.showinfo("Éxito", "Proveedor eliminado con éxito")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al eliminar el proveedor: {e}")  # Muestra un mensaje de error si ocurre un problema
        finally:
            conn.close()  # Cierra la conexión a la base de datos

        self.limpiar_treeview()  # Limpia el Treeview
        self.cargar_registros()  # Carga los registros nuevamente para reflejar los cambios

    def widgets(self): # Crea los widgets de la interfaz gráfica

        # Creación de las etiquetas y de los campos de entrada
        labelframe = tk.LabelFrame(self, text="Información Proveedores",
                                   font="sans 16 bold", bg="#477296", relief="raised", borderwidth=1) # Crea un marco para contener los widgets
        labelframe.place(x=5, y=30, width=1150, height=180)

        label_nombre = tk.Label( # Crea una etiqueta para el nombre
            labelframe, text="Nombre: ", font="sans 12 bold", bg="#477296")
        label_nombre.place(x=10, y=11)
        self.entry_nombre = ttk.Entry(labelframe, font="sans 12 bold")
        self.entry_nombre.place(x=145, y=8, width=200, height=30)

        label_cedula = tk.Label( # Crea una etiqueta para la cédula
            labelframe, text="Cédula Jurídica: ", font="sans 12 bold", bg="#477296")
        label_cedula.place(x=10, y=60)
        self.entry_cedula = ttk.Entry(labelframe, font="sans 12 bold") # Crea un campo de entrada para la cédula
        self.entry_cedula.place(x=145, y=57, width=200, height=30)

        label_direccion = tk.Label( # Crea una etiqueta para la dirección
            labelframe, text="Dirección: ", font="sans 12 bold", bg="#477296")
        label_direccion.place(x=10, y=110)
        self.entry_direccion = ttk.Entry(labelframe, font="sans 12 bold")
        self.entry_direccion.place(x=145, y=107, width=200, height=30)

        label_telefono = tk.Label( # Crea una etiqueta para el teléfono
            labelframe, text="Teléfono: ", font="sans 12 bold", bg="#477296")
        label_telefono.place(x=450, y=11)
        self.entry_telefono = ttk.Entry(labelframe, font="sans 12 bold")
        self.entry_telefono.place(x=620, y=8, width=200, height=30)

        label_correo = tk.Label( # Crea una etiqueta para el correo electrónico
            labelframe, text="Correo Electrónico: ", font="sans 12 bold", bg="#477296")
        label_correo.place(x=450, y=60)
        self.entry_correo = ttk.Entry(labelframe, font="sans 12 bold")
        self.entry_correo.place(x=620, y=58, width=200, height=30)

        label_cuenta = tk.Label( # Crea una etiqueta para la cuenta bancaria
            labelframe, text="Datos Bancarios: ", font="sans 12 bold", bg="#477296")
        label_cuenta.place(x=450, y=110)
        self.entry_cuenta = ttk.Entry(labelframe, font="sans 12 bold")
        self.entry_cuenta.place(x=620, y=107, width=200, height=30)

        # Funcion para cargar las imagenes de los botones
        imagen_pil = Image.open("iconos/registrar.png") # Carga la imagen
        imagen_resize = imagen_pil.resize((30, 30)) # Redimensiona la imagen
        imagen_tk_registrar = ImageTk.PhotoImage(imagen_resize) # Convierte la imagen a un formato compatible con Tkinter

        imagen_pil_editar = Image.open("iconos/editar.png") # Carga la imagen editar
        imagen_resize_editar = imagen_pil_editar.resize((30, 30))
        imagen_tk_editar = ImageTk.PhotoImage(imagen_resize_editar) # Convierte la imagen a un formato compatible con Tkinter

        imagen_tk_guardar =Image.open("iconos/guardar.png") # Carga la imagen guardar
        imagen_resize_guardar = imagen_tk_guardar.resize((30, 30))
        imagen_tk_guardar = ImageTk.PhotoImage(imagen_resize_guardar) # Convierte la imagen a un formato compatible con Tkinter

        imagen_tk_eliminar = Image.open("iconos/eliminar.png") # Carga la imagen eliminar
        imagen_resize_eliminar = imagen_tk_eliminar.resize((30, 30))
        imagen_tk_eliminar = ImageTk.PhotoImage(imagen_resize_eliminar) # Convierte la imagen a un formato compatible con Tkinter
        
        # Creación de los botones que se utilizan en la interfaz gráfica
        self.btn_registrar = ttk.Button(labelframe, text="Registrar", command=self.guardar_proveedor, style="TButton") # Crea un botón para registrar el proveedor
        self.btn_registrar.config(image=imagen_tk_registrar, compound=LEFT)
        self.btn_registrar.image = imagen_tk_registrar
        self.btn_registrar.place(x=850, y=15, width=124, height=50)

        self.btn_editar = ttk.Button(labelframe, text="Editar", command=self.editar_proveedor, style="TButton") # Crea un botón para editar el proveedor
        self.btn_editar.config(image=imagen_tk_editar, compound=LEFT)
        self.btn_editar.image = imagen_tk_editar
        self.btn_editar.place(x=990, y=15, width=124, height=50)

        self.btn_guardar = ttk.Button(labelframe, text="Guardar\nModificación", command=self.guardar_edicion, style="TButton")
        self.btn_guardar.config(image=imagen_tk_guardar, compound=LEFT)
        self.btn_guardar.image = imagen_tk_guardar
        self.btn_guardar.place(x=850, y=70, width=124, height=50)

        self.btn_eliminar = ttk.Button(labelframe, text="Eliminar", command=self.eliminar_proveedor, style="TButton") # Crea un botón para eliminar el proveedor
        self.btn_eliminar.config(image=imagen_tk_eliminar, compound=LEFT)
        self.btn_eliminar.image = imagen_tk_eliminar
        self.btn_eliminar.place(x=990, y=70, width=124, height=50)

        # Creación de la interfaz gráfica para mostrar los proveedores
        self.tree = ttk.Treeview(self, columns=(
            "Nombre", "Cedula", "Direccion", "Telefono", "Correo", "Cuenta"), show="headings") # Crea un Treeview para mostrar los proveedores
        for col in ("Nombre", "Cedula", "Direccion", "Telefono", "Correo", "Cuenta"):
            self.tree.heading(col, text=col)
        self.tree.place(x=5, y=220, width=1180, height=300)

        self.grid_rowconfigure(0, weight=0) # Configura el peso de la fila 0
        self.grid_rowconfigure(1, weight=1) # Configura el peso de la fila 1
        self.grid_columnconfigure(0, weight=1) # Configura el peso de la columna 0
