######################################################################################################################
# Nombre del programa:PROYECTO CARNCIERIA.PY
# Número del grupo de trabajo: 2 - Snake Coders
# Nombres de los programadores:
# Daniel Cordero Porras
# Marcos Vargas Hernandez
# Angelo Bermudez Ayales
# Fecha de elaboración del programa: XXXXX
# Versión del Python: 3.13.1
# Nombre del IDE donde se desarrollo el programa: Visual Studio Code
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
