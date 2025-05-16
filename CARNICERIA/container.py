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
# Importar librerías necesarias
from tkinter import *
import tkinter as tk
from punto_venta import Punto_Venta # Importar el módulo de Punto de Venta
from productos import Productos # Importar el módulo de Productos
from clientes import Clientes # Importar el módulo de Clientes
from proveedor import Proveedor # Importar el módulo de Proveedor
from inventario import Inventario # Importar el módulo de Inventario
from caja import Caja # Importar el módulo de Caja
from almacen import Almacen # Importar el módulo de Almacen
from pagos import Pagos # Importar el módulo de Pagos
from informacion import Informacion # Importar el módulo de Información
import sys
import os

"""
Clase Container: Esta clase es la encargada de crear el frame principal de la aplicación y de manejar los frames secundarios.
La clase hereda de tk.Frame y contiene métodos para mostrar los diferentes frames de la aplicación. 
Además, contiene métodos para crear los botones y labels que se utilizan en la interfaz gráfica.
"""

class Container(tk.Frame):
    def __init__(self, padre, controlador): # Constructor de la clase Container
        super().__init__(padre) # Inicializa la clase padre Frame
        self.controlador = controlador # Almacena el controlador
        self.pack() # Empaqueta el frame
        self.place(x=0, y=0, width=1200, height=700) # Coloca el frame en la posición (0,0) y le da un tamaño de 1200x700
        self.widgets() # Llama a la función widgets para crear los botones y labels
        self.frames = {} # Diccionario para almacenar los frames
        self.buttons = [] # Lista para almacenar los botones
        for i in (Punto_Venta, Productos, Clientes, Proveedor, Inventario, Caja, Almacen, Pagos, Informacion): # Itera sobre las clases de los frames
            # Crea una instancia de cada frame y lo almacena en el diccionario frames
            frame = i(self) # Crea una instancia del frame
            self.frames[i] = frame # Almacena el frame en el diccionario frames
            frame.pack() # Empaqueta el frame
            frame.config(bg="#477296", highlightbackground="gray", highlightthickness=1) # Configura el color de fondo y el borde del frame
            frame.place(x=0, y=40, width=1200, height=700)
        self.show_frames(Punto_Venta) # Muestra el frame de Punto de Venta al iniciar la aplicación

    # Función para mostrar los frames que se crean y los botones
    def show_frames(self, container): 
        frame = self.frames[container] 
        frame.tkraise()

    def punto_venta(self): # se va a mostrar el frame de punto de venta
        self.show_frames(Punto_Venta)

    def productos(self): # se va a mostrar el frame de productos
        self.show_frames(Productos)

    def clientes(self): # se va a mostrar el frame de clientes
        self.show_frames(Clientes)

    def proveedor(self): # se va a mostrar el frame de proveedor
        self.show_frames(Proveedor)

    def inventario(self): # se va a mostrar el frame de inventario
        self.show_frames(Inventario)

    def caja(self): # se va a mostrar el frame de caja
        self.show_frames(Caja)

    def almacen(self): # se va a mostrar el frame de almacen
        self.show_frames(Almacen)

    def pagos(self): # se va a mostrar el frame de pagos
        self.show_frames(Pagos)

    def informacion(self): # se va a mostrar el frame de informacion
        self.show_frames(Informacion)

     # se va a encapsular los botones y labels

    def widgets(self): # se va a crear el frame de los botones
        # Crear frame para los botones
        frame2 = tk.Frame(self)
        frame2.place(x=0,y=0,width=1200,height=150)

        self.btn_punto_venta = Button(frame2, fg="black", text="Punto Venta", font="sans 12 bold",relief="raised", borderwidth=5, command=self.punto_venta)
        self.btn_punto_venta.place(x=0, y=0, width=133, height=40 )

        self.btn_productos = Button(frame2, fg="black", text="Productos", font="sans 12 bold",relief="raised", borderwidth=5, command=self.productos)
        self.btn_productos.place(x=133, y=0, width=133, height=40)

        self.btn_clientes = Button(frame2, fg="black", text="Clientes", font="sans 12 bold", relief="raised", borderwidth=5, command=self.clientes)
        self.btn_clientes.place(x=266, y=0, width=133, height=40)

        #self.btn_pedidos = Button(frame2, fg="black", text="Pedidos", font="sans 12 bold", relief="raised", borderwidth=5, command=self.pedidos)
        #self.btn_pedidos.place(x=360, y=0, width=120, height=40)

        self.btn_proveedor = Button(frame2, fg="black", text="Proveedor", font="sans 12 bold", relief="raised", borderwidth=5, command=self.proveedor)
        self.btn_proveedor.place(x=399, y=0, width=133, height=40)

        self.btn_inventario = Button(frame2, fg="black", text="Inventario", font="sans 12 bold", relief="raised", borderwidth=5, command=self.inventario)
        self.btn_inventario.place(x=532, y=0, width=133, height=40)

        self.btn_caja = Button(frame2, fg="black", text="Caja", font="sans 12 bold", relief="raised", borderwidth=5, command=self.caja)
        self.btn_caja.place(x=665, y=0, width=133, height=40)

        self.btn_almacen = Button(frame2, fg="black", text="Almacen", font="sans 12 bold", relief="raised", borderwidth=5, command=self.almacen)
        self.btn_almacen.place(x=798, y=0, width=133, height=40)

        self.btn_pagos = Button(frame2, fg="black", text="Pagos", font="sans 12 bold", relief="raised", borderwidth=5, command=self.pagos)
        self.btn_pagos.place(x=931, y=0, width=133, height=40)

        self.btn_informacion = Button(frame2, fg="black", text="Información", font="sans 12 bold", relief="raised", borderwidth=5, command=self.informacion)
        self.btn_informacion.place(x=1064, y=0, width=133, height=40)

        self.buttons = [self.btn_punto_venta, self.btn_productos, self.btn_clientes, self.btn_proveedor,
                        self.btn_inventario, self.btn_caja, self.btn_almacen, self.btn_pagos, self.btn_informacion]
