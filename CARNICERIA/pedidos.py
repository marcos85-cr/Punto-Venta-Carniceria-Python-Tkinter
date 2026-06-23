######################################################################################################################
# Nombre del programa: PROYECTO CARNICERIA.PY
# Nombres del programador: [Marcos Vargas Hernández]
# Fecha de elaboración del programa: 14-04-2025
# Versión del Python: 3.13.2
# Nombre del IDE donde se desarrolló el programa: Visual Studio Code
######################################################################################################################
from tkinter import *
import tkinter as tk


class Pedidos(tk.Frame):

    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()

    def widgets(self):
        label = Label(self, text="Pedidos")
        label.pack()
