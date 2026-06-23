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
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import threading  # Nos ayuda a filtrar los articulos del inventario
import sys
import os

"""
Clase Productos: Esta clase se encarga de crear la ventana de productos, donde se pueden agregar, editar y eliminar productos.
La clase hereda de tk.Frame y contiene métodos para crear los widgets, cargar los productos desde la base de datos,
mostrar la información de los productos, y manejar eventos como la selección de un producto en el combobox.
"""

class Productos(tk.Frame):

    def __init__(self, padre): # Constructor de la clase Productos
        super().__init__(padre)
        self.widgets()
        self.articulos_combobox() # Crea el combobox para seleccionar los artículos
        self.cargar_articulos() # Carga los artículos desde la base de datos
        self.timer_articulos = None # Inicializa el temporizador para filtrar artículos

        # Ruta dinámica para la carpeta de imágenes
        base_path = os.path.dirname(__file__)
        self.image_folder = os.path.join(base_path, "fotos")
        os.makedirs(self.image_folder, exist_ok=True)  # Crea la carpeta si no existe

    def widgets(self):
     # ===================================PRIMER LABEL FRAME =============================================================#

        # Creacion de los frames del inventario
        # el Canvas posiciona las imagenes en el lable frame
        canvas_articulos = tk.LabelFrame(self, text="Artículos", font="Arial 14 bold", bg="#477296") 
        canvas_articulos.place(x=340, y=10, width=820, height=625)

        self.canvas = tk.Canvas(canvas_articulos, bg="#477296")
        self.scrollbar = tk.Scrollbar(canvas_articulos, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))) # se configura el scroll de desplazamiento) 
        
        # se crea el scroll de desplazamiento vertical
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw") # se crea la ventana dentro del canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set) # se configura el scroll de desplazamiento

        self.scrollbar.pack(side="right", fill="y") # se posiciona el scroll de desplazamiento a la derecha
        self.canvas.pack(side="left", fill="both", expand=True) # se posiciona el canvas a la izquierda y se expande para llenar el espacio disponible

     # ===================================SEGUNDO LABEL FRAME =============================================================#
        lblframe_buscar = LabelFrame(self, text="Buscar", relief="raised", borderwidth=1, font="Arial 14 bold", bg="#477296") # se crea el label frame para buscar articulos
        lblframe_buscar.place(x=10, y=10, width=305, height=80) # se posiciona el label frame en la ventana

        self.comboboxbuscar = ttk.Combobox(lblframe_buscar, font="Arial 12") # se crea el combobox para buscar articulos
        self.comboboxbuscar.place(x=5, y=5, width=290,  height=40)
        self.comboboxbuscar.bind("<<ComboboxSelected>>", self.on_combobox_selec) # actualiza informacion de los frames de inventario
        self.comboboxbuscar.bind("<KeyRelease>", self.filtrar_articulos) # se filtran los articulos al escribir en el combobox

     # ====================================TERCER LABELFRAME " Selección"================================================================#
        lblframe_seleccion = LabelFrame(self, text="Selección", relief="raised", borderwidth=1, font="Arial 18 bold", bg="#477296") # se crea el label frame para seleccionar articulos
        lblframe_seleccion.place(x=10, y=95, width=305, height=190)

        # Se crean etiquetas y entadas para ver el estatus de cada articulo seleccionado
        self.label1 = tk.Label(lblframe_seleccion, text="Artículo:", font="Arial 16", bg="#477296", wraplength=300)
        self.label1.place(x=5, y=5)

        self.label2 = tk.Label(lblframe_seleccion, text="Precio ₵:", font="Arial 16", bg="#477296",) 
        self.label2.place(x=5, y=40)

        self.label3 = tk.Label(lblframe_seleccion, text="Costo ₵:", font="Arial 16", bg="#477296",)
        self.label3.place(x=5, y=70)

        self.label4 = tk.Label(lblframe_seleccion, text="Stock:", font="Arial 16", bg="#477296",)
        self.label4.place(x=5, y=100)

        self.label5 = tk.Label(lblframe_seleccion, text="Estado:", font="Arial 16", bg="#477296",) #
        self.label5.place(x=5, y=130)
     # ====================================CUARTO LABELFRAME BOTONES ================================================================#

        # imagen boton Agregar
        imagen_pil = Image.open("iconos/agregar.png")
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk_agregar = ImageTk.PhotoImage(imagen_resize)

        # imagen boton Editar
        imagen_pil = Image.open("iconos/editar.png")
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk_editar = ImageTk.PhotoImage(imagen_resize)

        # imagen boton Eliminar
        imagen_pil = Image.open("iconos/eliminar.png")
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk_eliminar = ImageTk.PhotoImage(imagen_resize)


        lblframe_botones = LabelFrame(self, bg="#477296", highlightthickness=0, relief="flat", borderwidth=0, text="Opciones", font="Arial 14 bold") # se crea el label frame para los botones
        lblframe_botones.place(x=10, y=290, width=305, height=300)

        btn1 = tk.Button(lblframe_botones, text="Agregar", bg="#D3D3D3", highlightthickness=0, relief="flat", borderwidth=0, font="Arial 14 bold", command=self.agregar_articulo)
        btn1.config(image=imagen_tk_agregar, compound=LEFT, padx=15)
        btn1.image = imagen_tk_agregar
        btn1.place(x=20, y=20, width=180, height=40)

        btn2 = tk.Button(lblframe_botones, text="Editar", bg="#D3D3D3", highlightthickness=0, relief="flat", borderwidth=0, font="Arial 14 bold", command=self.editar_articulos)
        btn2.config(image=imagen_tk_editar, compound=LEFT, padx=15)
        btn2.image = imagen_tk_editar
        btn2.place(x=20, y=80, width=180, height=40)

        btn3 = tk.Button(lblframe_botones, text="Eliminar", bg="#D3D3D3", highlightthickness=0, relief="flat", borderwidth=0, font="Arial 14 bold", command=self.eliminar_articulo)
        btn3.config(image=imagen_tk_eliminar, compound=LEFT, padx=15)
        btn3.image = imagen_tk_eliminar
        btn3.place(x=20, y=140, width=180, height=40)

    # Se crea el metodo para cargar imagenes a los productos
    def laod_image(self):
        file_path = filedialog.askopenfilename()
        if file_path: # Verifica si se seleccionó un archivo
            try:
                # Ruta dinámica para guardar la imagen
                base_path = os.path.dirname(__file__) # Obtiene la ruta del directorio actual
                self.image_folder = os.path.join(base_path, "fotos")
                os.makedirs(self.image_folder, exist_ok=True) # Crea la carpeta si no existe

                # Redimensionar y guardar la imagen
                image = Image.open(file_path)
                image_name = os.path.basename(file_path)
                image = image.resize((200, 200), Image.LANCZOS)
                image_save_path = os.path.join(self.image_folder, image_name)
                image.save(image_save_path)

                # Cargar la imagen en Tkinter
                self.image_tk = ImageTk.PhotoImage(image)
                self.product_image = self.image_tk
                self.image_path = image_save_path

                # Mostrar la imagen en el frame
                img_label = tk.Label(self.frameimg, image=self.image_tk)
                img_label.place(x=0, y=0, width=200, height=200)
            except Exception as e:
                print(f"Error al cargar la imagen: {e}")
                messagebox.showerror("Error", "No se pudo cargar la imagen")

    def articulos_combobox(self): # Crea el combobox para seleccionar los artículos
        self.con = sqlite3.connect('database.db') # Conecta a la base de datos
        self.cur = self.con.cursor()
        self.cur.execute("SELECT articulos FROM articulos") # Selecciona los artículos de la base de datos
        self.articulos = [row[0] for row in self.cur.fetchall()] # Obtiene los artículos de la base de datos
        self.comboboxbuscar['values'] = self.articulos # Asigna los artículos al combobox

    def agregar_articulo(self): # Crea la ventana para agregar un artículo al utilizar el botón "Agregar"
        top = tk.Toplevel(self)
        top.title("Agregar Artículo")
        top.geometry("700x400+200+50")
        top.config(bg="#477296")
        top.resizable(False, False) # Para que no se puede redimencionar una ventana
        top.transient(self.master) # Para que la ventana se mantenga encima de la ventana principal
        top.grab_set() # Para que la ventana se mantenga activa
        top.focus_set() # Para que la ventana se mantenga activa
        top.lift() # Para que la ventana se mantenga activa

        # Se crean etiquetas y entradas para agregar un artículo
        tk.Label(top, text="Artículo: ", font="Arial 12 bold", bg="#477296").place(x=20, y=20, width=80, height=25)
        entry_articulo = ttk.Entry(top, font="Arial 12 bold")
        entry_articulo.place(x=120, y=20, width=250, height=30)

        tk.Label(top, text="Precio ₵: ", font="arias 12 bold", bg="#477296").place(x=20, y=60, width=80, height=25)
        entry_precio = ttk.Entry(top, font="Arial 12 bold")
        entry_precio.place(x=120, y=60, width=250, height=30)

        tk.Label(top, text="Costo ₵: ", font="arias 12 bold", bg="#477296").place(x=20, y=100, width=80, height=25)
        entry_costo = ttk.Entry(top, font="Arial 12 bold")
        entry_costo.place(x=120, y=100, width=250, height=30)

        tk.Label(top, text="Stock: ", font="arias 12 bold", bg="#477296").place(x=20, y=140, width=80, height=25)
        entry_stock = ttk.Entry(top, font="Arial 12 bold")
        entry_stock.place(x=120, y=140, width=250, height=30)

        tk.Label(top, text="Estado: ", font="arias 12 bold", bg="#477296").place(x=20, y=180, width=80, height=25)
        entry_estado = ttk.Entry(top, font="Arial 12 bold")
        entry_estado.place(x=120, y=180, width=250, height=30)

        self.frameimg = tk.Frame(top, bg="white", highlightbackground="gray", highlightthickness=1)
        self.frameimg.place(x=440, y=30, width=200, height=200)

        btnimage = tk.Button(top, text="Cargar imagen", bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296",  font="Arial 12 bold", command=self.laod_image)
        btnimage.place(x=470, y=260, width=150, height=40)

        # Se crea la funcion guardar en artículos
        def guardar(): 
            articulos = entry_articulo.get() # Obtiene el nombre de cada uno de las entradas
            precio = entry_precio.get()
            costo = entry_costo.get()
            stock = entry_stock.get()
            estado = entry_estado.get()

            if not articulos or not precio or not costo or not stock or not estado:
                messagebox.showerror("Error", "Todos los campos deben ser completados")
                return
            try:
                precio = float(precio) # Convierte el precio a float
                costo = float(costo)
                stock = int(stock) # Convierte el stock a int
            except ValueError:
                messagebox.showerror("Error", "precio, costo, stock deben ser números validos")
                return
            
            base_path = os.path.dirname(__file__)  # Obtiene la ruta del directorio actual
            if hasattr(self, 'image_path'):  # Guarda la imagen
                image_path = self.image_path
            else:
                # los articulos que no tienen fotos, se les pone automaticamente esto
                image_path = os.path.join(base_path, "fotos","default.png")

            try:
                self.cur.execute("INSERT INTO articulos (articulos, precio, costo, stock, estado, image_path) VALUES (?, ?, ?, ?, ?, ?)",  # Inserta los datos a la base de datos
                                 (articulos, precio, costo, stock, estado, image_path))
                self.con.commit()                                             # Guarda los cambios en la base de datos
                messagebox.showinfo("Exito", "Artículo agregado correctamente")
                top.destroy()         # Cierra la ventana de agregar artículo
                self.cargar_articulos() # Carga los artículos desde la base de datos
                self.articulos_combobox() # Carga los artículos en el combobox
            except sqlite3.Error as e:
                print("Error al cargar el artículo", e)
                messagebox.showerror("Error", "Error al agregar el artículo")

        # Guarda el artículo al hacer clic en el botón "Guardar"
        tk.Button(top, text="Guardar", font="Arial 12 bold", bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296", command=guardar).place(x=50, y=260, width=150, height=40)  
        tk.Button(top, text="Cancelar", font="Arial 12 bold", bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296", command=top.destroy).place(x=260, y=260, width=150, height=40)

    #Funcion que cargar los articulos para mostrarlos en pantalla
    def cargar_articulos(self, filtro=None, categoria=None):
        self.after(0, self._cargar_articulos, filtro, categoria)
        
    def _cargar_articulos(self, filtro=None, categoria=None): # Carga los artículos desde la base de datos
        for widget in self.scrollable_frame.winfo_children(): # Elimina los widgets existentes en el frame
            widget.destroy()

        query = "SELECT articulos, precio, image_path FROM articulos" # Consulta para obtener los artículos de la base de datos
        params = [] # Lista para almacenar los parámetros de la consulta

        if filtro: # Si se proporciona un filtro, se agrega a la consulta
            query += " WHERE articulos LIKE ?" # Se agrega la cláusula WHERE a la consulta
            params.append(f'%{filtro}%') # Se muestra los datos cuando se ingresa el nombre en el combobox

        try:
            with sqlite3.connect('database.db') as con: # Conecta a la base de datos
                cur = con.cursor()
                cur.execute(query, params)
                articulos = cur.fetchall()

            self.row = 0
            self.column = 0

            for articulos, precio, image_path in articulos: 
                self.mostrar_articulo(articulos, precio, image_path) # Muestra los artículos en el frame
        except sqlite3.Error as e:
            print(f"Error al cargar los artículos: {e}")
            messagebox.showerror("Error", "No se pudieron cargar los artículos")

    # Funcion para mostrar las imagenes en el inventario
    def mostrar_articulo(self, articulo, precio, image_path):
        article_frame = tk.Frame(self.scrollable_frame, bg="white", relief="solid", bd=1, highlightbackground="white", highlightthickness=1)
        article_frame.grid(row=self.row, column=self.column, padx=55, pady=10)

        if not image_path or not os.path.exists(image_path): # Verifica si la imagen existe
            base_path = os.path.dirname(__file__)  # Obtiene la ruta del directorio actual
            image_path = os.path.join(base_path, "fotos", "default.png")  # Ruta de la imagen por defecto
        try:
            image = Image.open(image_path) 
            image = image.resize((150, 150), Image.LANCZOS)
            image = ImageTk.PhotoImage(image)
            image_label = tk.Label(article_frame, image=image, borderwidth=0) # Crea la etiqueta para mostrar la imagen
            image_label.image = image  # Evita que se borre la imagen
            image_label.pack(expand=True, fill="both") # Muestra la imagen en el frame
            image_label.bind("<Button-1>", lambda e: self.mostrar_info_producto(articulo)) # Muestra la información del producto al hacer clic en la imagen
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            
        name_label = tk.Label(article_frame, text=articulo, bg="white", fg = "black", anchor="w", wraplength=150, font="Arial 10 bold") 
        name_label.pack(side="top", fill="x")

        precio_label = tk.Label(article_frame, text=f"Precio: ₵{precio:,.2f}", bg="white", fg="black", anchor="w", wraplength=150, font="Arial 10 bold")
        precio_label.pack(side="bottom", fill="x")

        # Cada 3 artículos se crea una fila nueva para el acomodo de los artículos
        self.column += 1 # Incrementa la columna para el siguiente artículo
        if self.column > 3: # Si hay más de 3 artículos en la fila, se reinicia la columna y se incrementa la fila
            self.column = 0
            self.row += 1

    def mostrar_info_producto(self, articulo): # Muestra la información del producto al hacer clic en la imagen
        try:
            self.cur.execute(
                "SELECT articulos, precio, costo, stock, estado FROM articulos WHERE articulos=?", (articulo,)) # Selecciona el artículo de la base de datos
            resultado = self.cur.fetchone() # Obtiene el artículo de la base de datos

            if resultado is not None:
                articulos, precio, costo, stock, estado = resultado # Desempaqueta el resultado de la consulta

                # Actualiza los labels en lblframe_seleccion
                self.label1.config(text=f"Artículo: {articulos}") 
                self.label2.config(text=f"Precio ₵: {precio}")
                self.label3.config(text=f"Costo ₵: {costo}")
                self.label4.config(text=f"Stock: {stock}")
                self.label5.config(text=f"Estado: {estado}")
                if estado.lower() == "activo":
                    self.label5.config(fg="white")
                elif estado.lower() == "inactivo":
                    self.label5.config(fg="red")
                else:
                    self.label5.config(fg="black")
            else:
                self.label1.config(text="Artículo: No encontrado") # Se muestra un mensaje si no se encuentra el artículo
                self.label2.config(text="Precio ₵: N/A")
                self.label3.config(text="Costo ₵: N/A")
                self.label4.config(text="Stock: N/A")
                self.label5.config(text="Estado: N/A", fg="black")

        except sqlite3.Error as e:
            print("Error al obtener los datos del artículo", e)
            messagebox.showerror(
                "Error", "Error al obtener los datos del artículo")

    # Funciones que actualizan en el inventario la información de cada producto
    def on_combobox_selec(self, event): 
        self.actualizar_label() # Actualiza los labels en lblframe_seleccion al seleccionar un artículo del combobox

    def actualizar_label(self, event=None): # Actualiza los labels en lblframe_seleccion al seleccionar un artículo del combobox
        articulo_seleccionado = self.comboboxbuscar.get()

        try:
            self.cur.execute("SELECT articulos, precio, costo, stock, estado FROM articulos WHERE articulos=?", (articulo_seleccionado,))
            resultado = self.cur.fetchone() # Obtengo todo la información de la consulta

            if resultado is not None:
                articulos, precio, costo, stock, estado = resultado # Desempaqueta el resultado de la consulta

                # se van actualizar los label del inventario
                self.label1.config(text=f"Articulo: {articulos}")
                self.label2.config(text=f"Precio: {precio}")
                self.label3.config(text=f"Costo: {costo}")
                self.label4.config(text=f"Stock: {stock}")

                self.label5.config(text=f"Estado: {estado}")
                if estado.lower() == "activo":
                    self.label5.config(fg="white") # Si existe inventario aparece el texto estado Activo en blanco
                elif estado.lower() == "inactivo":
                    self.label5.config(fg="red")  # Si no existe inventario aparece el texto estado Inactivo en rojo
                else:
                    self.label5.config(fg="black")

            else:
                self.label1.config(text="Articulo: No encontrado")
                self.label2.config(text="Precio: N/A")
                self.label3.config(text="Costo:  N/A")
                self.label4.config(text="Stock:  N/A")
                self.label5.config(text="Estado:  N/A", fg="black")

        except sqlite3.Error as e:
            print("Error al obtener los datos del articulo", e)
            messagebox.showerror("Error", "Error al obtener los datos del articulo")

    def filtrar_articulos(self, event): # Filtra los artículos al escribir en el combobox
        if self.timer_articulos:
            self.after_cancel(self.timer_articulos)
        self.timer_articulos = self.after(500, self._filter_articulos) # Llama a la función _filter_articulos después de 500 ms

    def _filter_articulos(self): # Filtra los artículos al escribir en el combobox
        typed = self.comboboxbuscar.get() # Obtiene el texto ingresado en el combobox

        if typed == '': # Si el combobox de articulos esta vacio muestra todos los datos
            data = self.articulos # Se muestra todos los articulos
        else:
            data = [item for item in self.articulos if typed.lower() in item.lower()] # Filtra los artículos que contienen el texto ingresado
        
        if data:
            self.comboboxbuscar['values'] = data # Asigna los artículos filtrados al combobox
            self.comboboxbuscar.event_generate('<Down>') # genera lista con datos encontrado y despliega lista
        else: 
            self.comboboxbuscar['values'] = ['No se encontraron resultados'] # Si no se encuentran resultados, muestra un mensaje en el combobox
        
        self.cargar_articulos(filtro=typed) # Llama a la función cargar_articulos para mostrar los artículos filtrados

    def editar_articulos(self): # Crea la ventana para editar un artículo al utilizar el botón "Editar"
        selected_item = self.comboboxbuscar.get() # Obtiene el artículo seleccionado en el combobox

        if not selected_item: # Si no se selecciona un artículo, muestra un mensaje de error
            messagebox.showerror("Error", " Selecciona un artículo para editar")
            return
        self.cur.execute("SELECT articulos, precio, costo, stock, estado, image_path FROM articulos WHERE articulos=?", (selected_item,) )
        resultado = self.cur.fetchone() # Obtiene el artículo de la base de datos

        if not resultado:
            messagebox.showerror("Error", " Artículo no encontrado") # Si no se encuentra el artículo, muestra un mensaje de error
            return

        # Crea la ventana para agregar el artículo
        top = tk.Toplevel(self)
        top.title("Agregar Artículo")
        top.geometry("700x400+200+50") # Configura el tamaño y la posición de la ventana
        top.config(bg="#477296") # Configura el color de fondo de la ventana
        top.resizable(False, False) # Para que no se puede redimencionar una ventana
        top.transient(self.master) # Para que la ventana se mantenga encima de la ventana principal
        top.grab_set() # Para que la ventana se mantenga activa
        top.focus_set() # Para que la ventana se mantenga activa
        top.lift()

        (articulos, precio, costo, stock, estado, image_path) = resultado  # se desempaquetan los articulos

        tk.Label(top, text="Articulos: ", font="Arial 12 bold", bg="#477296").place(x=20, y=20, width=80, height=25)
        entry_articulo = ttk.Entry(top, font="Arial 12 bold")
        entry_articulo.place(x=120, y=20, width=250, height=30)
        entry_articulo.insert(0, articulos)

        tk.Label(top, text="Precio: ", font="Arial 12 bold", bg="#477296").place(x=20, y=60, width=80, height=25)   # Se crea la etiqueta para el precio
        entry_precio = ttk.Entry(top, font="Arial 12 bold")
        entry_precio.place(x=120, y=60, width=250, height=30)
        entry_precio.insert(0, precio)

        tk.Label(top, text="Costo: ", font="Arial 12 bold", bg="#477296").place(x=20, y=100, width=80, height=25) # Se crea la etiqueta para el costo
        entry_costo = ttk.Entry(top, font="Arial 12 bold")
        entry_costo.place(x=120, y=100, width=250, height=30)
        entry_costo.insert(0, costo)

        tk.Label(top, text="Stock: ", font="Arial 12 bold", bg="#477296").place(x=20, y=140, width=80, height=25) # Se crea la etiqueta para el stock
        entry_stock = ttk.Entry(top, font="Arial 12 bold")
        entry_stock.place(x=120, y=140, width=250, height=30)
        entry_stock.insert(0, stock)
        
        tk.Label(top, text="Estado: ", font="Arial 12 bold", bg="#477296").place(x=20, y=180, width=80, height=25) # Se crea la etiqueta para el estado
        entry_estado = ttk.Entry(top, font="Arial 12 bold")
        entry_estado.place(x=120, y=180, width=250, height=30)
        entry_estado.insert(0, estado)

        self.frameimg = tk.Frame(top, bg="white", highlightbackground="gray", highlightthickness=1) # Crea el frame para mostrar la imagen
        self.frameimg.place(x=440, y=30, width=200, height=200)

        if image_path and os.path.exists(image_path): ## Si existe la imagen, la carga
            image = Image.open(image_path)
            image = image.resize((200, 200), Image.LANCZOS)  # Cambiar image_path por una tupla con las dimensiones
            self.product_image = ImageTk.PhotoImage(image)
            self.image_path = image_path
            image_label = tk.Label(self.frameimg, image=self.product_image)
            image_label.pack(expand=True, fill="both")

        # Crea el botón para cargar la imagen
        btnimagen = tk.Button(top, text="Cargar Imagen", bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296", font="Arial 12 bold", command=self.laod_image)
        btnimagen.place(x=470, y=260, width=150, height=40)

        def guardar(): # Guarda los cambios realizados al artículo
            nuevo_articulo = entry_articulo.get() # Obtiene cada uno de los datos de las entradas
            precio = entry_precio.get()
            costo = entry_costo.get()
            stock = entry_stock.get()
            estado = entry_estado.get()

            if not nuevo_articulo or not precio or not costo or not stock or not estado:  # Verifica si los campos están vacíos
                messagebox.showerror("Error", "Todos los campos deben ser completados") 
                return

            try:
                precio = float(precio) # Convierte el precio a float
                costo = float(costo)
                stock = int(stock) # Convierte el stock a int
            except ValueError:
                messagebox.showerror("Error", "Precio, costo y stock deben ser números validos")

            if hasattr(self, 'image_path'): # Verifica si se ha cargado una imagen
                image_path = self.image_path # Ruta de la imagen cargada
            else:
                image_path = (r"fotos/default.png") # Ruta de la imagen por defecto
            
            self.cur.execute("UPDATE articulos SET articulos=?, precio=?, costo=?, stock=?, image_path=?, estado=? WHERE articulos=?",
                            (nuevo_articulo, precio, costo, stock, image_path, estado, selected_item)) # Actualiza los datos del artículo en la base de datos
            self.con.commit() # Guarda los cambios en la base de datos

            self.articulos_combobox() # Actualiza el combobox con los artículos

            self.after(0, lambda:self.cargar_articulos(filtro=nuevo_articulo)) # Llama a la función cargar_articulos para mostrar los artículos filtrados

            top.destroy()
            messagebox.showinfo("Exito", "Artículo editado exitosamente" )

        btn_guardar = tk.Button(top, text="Guardar", bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296", font="Arial 12 bold", command=guardar)
        btn_guardar.place(x=260, y=260, width=150, height= 40)

    def eliminar_articulo(self): # Crea la ventana para eliminar un artículo al utilizar el botón "Eliminar"
        selected_item = self.comboboxbuscar.get() # Obtiene el artículo seleccionado en el combobox

        if not selected_item:
            messagebox.showerror("Error", "Selecciona un artículo para eliminar")
            return

        respuesta = messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar el artículo '{selected_item}'?") # Pregunta al usuario si está seguro de eliminar el artículo
        if respuesta: # Si el usuario confirma la eliminación
            try:
                self.cur.execute("DELETE FROM articulos WHERE articulos=?", (selected_item,)) # Elimina el artículo de la base de datos
                self.con.commit() # Guarda los cambios en la base de datos
                messagebox.showinfo("Éxito", "Artículo eliminado correctamente") # Muestra un mensaje de éxito
                self.articulos_combobox() # Actualiza el combobox con los artículos
                self.cargar_articulos() # Llama a la función cargar_articulos para mostrar los artículos filtrados
            except sqlite3.Error as e:
                print("Error al eliminar el artículo", e)
                messagebox.showerror("Error", "Error al eliminar el artículo")







