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
import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox # Libreria para crear ventanas emergentes
from container import Container
from PIL import Image, ImageTk # Libreria para cargar imagenes
import os # Libreria para manejar rutas de archivos

"""
Este programa es un sistema de gestión de carnicería que permite a los usuarios iniciar sesión y registrarse.
El sistema utiliza una base de datos SQLite para almacenar la información de los usuarios.  
El programa está diseñado para ser fácil de usar y proporciona una interfaz gráfica intuitiva.
El sistema incluye funciones de inicio de sesión y registro, así como la capacidad de mostrar una ventana principal con opciones adicionales.
El programa está diseñado para ser escalable y se pueden agregar más funciones en el futuro.
El código está estructurado en clases y métodos para facilitar la lectura y el mantenimiento.
"""


# Clase Login que hereda de tk.Frame
# Esta clase se encarga de gestionar el inicio de sesión y el registro de usuarios
class Login(tk.Frame): # Clase Login
    db_name = "database.db"

    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.pack()
        self.place(x=0, y=0, width=1200, height=700)
        self.controlador = controlador
        self.widgets()

    # Validación de Usuario y contraseña
    def validacion(self, user, pas): # Verifica si el usuario y la contraseña no están vacíos
        return len(user) > 0 and len(pas) > 0 #

    def login(self): # Método para iniciar sesión
        # Se obtienen los valores de usuario y contraseña
        user = self.username.get() # Obtiene el nombre de usuario
        pas = self.password.get() # Obtiene la contraseña
        # Se verifica si los campos de usuario y contraseña están llenos

        if self.validacion(user, pas): # Llama a la función de validación
            # Se prepara la consulta SQL para verificar el usuario y la contraseña
            consulta = "SELECT * FROM usuarios  WHERE username = ? AND password = ?" 
            parametros = (user, pas) # Se asignan los parámetros a la consulta

            # Se realiza consulta a la base de datos
            try: 
                with sqlite3.connect(self.db_name) as conn: # Conecta a la base de datos
                    # Se crea un cursor para ejecutar la consulta
                    cursor = conn.cursor()
                    cursor.execute(consulta, parametros) # Ejecuta la consulta
                    # Se obtienen los resultados de la consulta
                    result = cursor.fetchall()

                    if result:
                        self.control1() # Si el usuario y la contraseña son correctos, llama al controlador 1
                    else:
                        # Limpia los campos de usuario y contraseña
                        self.username.delete(0, 'end') 
                        self.password.delete(0, 'end') 
                        messagebox.showerror(title="Error", message="Usuario o contraseña incorrecta")
            except sqlite3.Error as e: # Captura cualquier error de la base de datos
                # Muestra un mensaje de error si no se pudo conectar a la base de datos
                messagebox.showerror(title="Error", message="No se conecto a la base de datos: {}".format(e))
        else: # Si los campos de usuario y contraseña no están llenos
            # Limpia los campos de usuario y contraseña
            messagebox.showerror(title="Error", message="Llene todas las casillas")

    def control1(self): 
        # Este controlador se utiliza con el boton iniciar
        self.controlador.show_frame(Container) # llama al frame de la ventana principal

    def control2(self): #
        # Este controlador con el boton registrar
        self.controlador.show_frame(Registro) # Llama al frame de registro

    def widgets(self): # Método para crear los widgets de la ventana de inicio de sesión
        # Crea un marco de fondo para la ventana de inicio de sesión
        fondo = tk.Frame(self, bg="#477296")
        fondo.pack()
        fondo.place(x=0, y=0, width=1200, height=700)

        base_path = os.path.dirname(__file__) # Obtiene la ruta del directorio actual

        # imagen bajo el cuadro de login
        # Carga la imagen del login
        ruta_bg = os.path.join(base_path, "imagenes/login.jpeg") # Crea la ruta completa de la imagen
        self.bg_image = Image.open(ruta_bg) # Abre la imagen
        self.bg_image = self.bg_image.resize((1200, 700)) # Redimensiona la imagen
        # Convierte la imagen a un formato compatible con Tkinter
        self.bg_image = ImageTk.PhotoImage(self.bg_image) 
        self.bg_label = ttk.Label(fondo, image=self.bg_image) # Crea una etiqueta para mostrar la imagen
        # Coloca la etiqueta de la imagen en el marco de fondo
        self.bg_label.place(x=0, y=0, width=1200, height=700) # posiciona la imagen

        # Frame principal donde se coloca el logo y los botones
        frame1 = tk.Frame(self, bg="#477296", highlightbackground="black", highlightthickness=1) 
        frame1.place(x=400, y=70, width=400, height=600)

        # Carga la imagen del logo
        ruta_logo = os.path.join(base_path, "imagenes/logo.jpeg") # Crea la ruta completa de la imagen
        self.logo_image = Image.open(ruta_logo) # Abre la imagen
        self.logo_image = self.logo_image.resize((200, 200)) # Redimensiona la imagen
        self.logo_image= ImageTk.PhotoImage(self.logo_image) # Convierte la imagen a un formato compatible con Tkinter
        self.logo_image_label = ttk.Label(frame1, image=self.logo_image , background="#477296") # Crea una etiqueta para mostrar la imagen
        self.logo_image_label.place(x=100, y=20, ) # posiciona la imagen

        # Creación ingresar con un login
        # Creación del espacio donde se ingresa el usuario
        user = ttk.Label(frame1, text="Nombre de Usuario", font="Arial 16 bold", background="#477296") 
        user.place(x=100, y=250)
        self.username = ttk.Entry(frame1, font="Arial 16 bold") # Crea un campo de entrada para el nombre de usuario
        self.username.place(x=80, y=290, width=240, height=40)

        # creación de espacio donde se ingresa el password
        pas = ttk.Label(frame1, text="Contraseña", font="Arial 16 bold", background="#477296")
        pas.place(x=100, y=340)
        self.password = ttk.Entry(frame1, show="*", font="Arial 16 bold")
        self.password.place(x=80, y=380, width=240, height=40)

        # Creación de botones para el login
        btn1 = tk.Button(frame1, text="Ingresar", font="Arial 16 bold", command=self.login)
        btn1.place(x=80, y=440, width=240, height=40)

        btn2 = tk.Button(frame1, text="Registrar", font="Arial 16 bold", command=self.control2) # Boton para registrar
        # Coloca el botón de registrar en el marco de inicio de sesión
        btn2.place(x=80, y=500, width=240, height=40)


class Registro(tk.Frame): # Clase Registro
    # Esta clase se encarga de gestionar el registro de nuevos usuarios
    db_name = "database.db"

    def __init__(self, padre, controlador):
        super().__init__(padre) # Inicializa la clase padre
        # Se empaqueta y se coloca el frame en la ventana principal
        self.pack()
        self.place(x=0, y=0, width=1200, height=650)
        self.controlador = controlador
        self.widgets()
    
    # Validación de Usuario y contraseña
    def validacion(self, user, pas): # Verifica si el usuario y la contraseña no están vacíos
        # Se verifica si los campos de usuario y contraseña están llenos
        return len(user) > 0 and len(pas) > 0
    
    def eje_consulta(self, consulta, parametros=()): # Método para ejecutar consultas SQL
        # Este método se encarga de ejecutar consultas SQL en la base de datos
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(consulta, parametros)
                conn.commit
        except sqlite3.Error as e:
            messagebox.showerror(title="Error", message="Error al ejecutar la consulta: {}".format(e)) # encapsula el error para mostrar
    
    def registro(self, ): # Método para registrar un nuevo usuario
        # Se obtienen los valores de usuario, contraseña y código de registro
        user = self.username.get() # Obtiene el nombre de usuario
        pas = self.password.get() # Obtiene la contraseña
        key = self.key.get() # Obtiene el código de registro
        # Se verifica si los campos de usuario y contraseña están llenos
        if self.validacion(user, pas): 
            if len(pas) < 6: # Verifica si la contraseña es menor a 6 caracteres
                # Si la contraseña es menor a 6 caracteres, muestra un mensaje de error
                messagebox.showinfo(title="Error", message="contraseña demasiado corta")
                self.username.delete(0, 'end') # Limpia el campo de usuario
                self.password.delete(0, 'end') # Limpia el campo de contraseña
            else:
                if key =="1234": # Codigo de aprovacion para nuevo usuario
                    consulta = "INSERT INTO usuarios VALUES (?,?,?)" # Consulta SQL para insertar un nuevo usuario
                    # Se asignan los parámetros a la consulta
                    parametros = (None, user, pas)
                    self.eje_consulta(consulta, parametros) # Llama al método para ejecutar la consulta
                    # Limpia los campos de usuario y contraseña
                    self.control1() 
                else:
                    messagebox.showerror(title="Registro", message="Error al ingresar el codigo de registro")
        else:
            messagebox.showerror(title="Error", message="Digitar sus datos")
    
    def control1(self): # Método para cambiar al frame de inicio de sesión
        # Este controlador se utiliza con el boton iniciar
        self.controlador.show_frame(Container)

    def control2(self): # Método para cambiar al frame de inicio de sesión
        # Este controlador se utiliza con el boton regresar
        self.controlador.show_frame(Login)


    def widgets(self): # Método para crear los widgets de la ventana de registro
        # Crea un marco de fondo para la ventana de registro
        fondo = tk.Frame(self, bg="#477296")
        fondo.pack()
        fondo.place(x=0, y=0, width=1200, height=650)

        # imagen bajo el cuadro de login
        # Carga la imagen del login
        self.bg_image = Image.open("imagenes/login.jpeg") # Abre la imagen
        # Redimensiona la imagen
        self.bg_image = self.bg_image.resize((1200, 650))
        self.bg_image = ImageTk.PhotoImage(self.bg_image) # Convierte la imagen a un formato compatible con Tkinter
        # Crea una etiqueta para mostrar la imagen
        self.bg_label = ttk.Label(fondo, image=self.bg_image)   # Crea una etiqueta para mostrar la imagen
        # Coloca la etiqueta de la imagen en el marco de fondo
        self.bg_label.place(x=0, y=0, width=1200, height=650)

        frame1 = tk.Frame(self, bg="#477296", highlightbackground="black", highlightthickness=1) # Crea un marco de fondo para la ventana de registro
        frame1.place(x=400, y=10, width=400, height=800)

        # Carga la imagen del logo
        self.logo_image = Image.open("imagenes/logo.jpeg") # Abre la imagen
        self.logo_image = self.logo_image.resize((200, 200)) # Redimensiona la imagen
        self.logo_image = ImageTk.PhotoImage(self.logo_image) 
        self.logo_image_label = ttk.Label(frame1, image=self.logo_image, background="#477296")
        self.logo_image_label.place(x=100, y=20, )

        # Creación ingresar con un login
        # Creación del espacio donde se ingresa el usuario
        user = ttk.Label(frame1, text="Nombre de Usuario", font="Arial 16 bold", background="#477296")
        user.place(x=80, y=250)
        self.username = ttk.Entry(frame1, font="Arial 16 bold")
        self.username.place(x=80, y=290, width=240, height=40)

        # creación de espacio donde se ingresa el password
        pas = ttk.Label(frame1, text="Contraseña", font="Arial 16 bold", background="#477296")
        pas.place(x=100, y=340)
        self.password = ttk.Entry(frame1, show="*", font="Arial 16 bold")
        self.password.place(x=80, y=380, width=240, height=40)

        key = ttk.Label(frame1, text="Código de Registro", font="Arial 16 bold", background="#477296")
        key.place(x=100, y=430)
        self.key = ttk.Entry(frame1, show="*", font="Arial 16 bold")
        self.key.place(x=80, y=470, width=240, height=40)

        # Creación de botones para el login
        btn3 = tk.Button(frame1, text="Registrarse", font="Arial 16 bold", command=self.registro)
        btn3.place(x=80, y=520, width=240, height=40)

        btn4 = tk.Button(frame1, text="Regresar", font="Arial 16 bold", command=self.control2)
        btn4.place(x=80, y=570, width=240, height=40)
