######################################################################################################################
# Nombre del programa: PROYECTO CARNICERIA.PY
# Nombres del programador: [Marcos Vargas Hernández]
# Fecha de elaboración del programa: 14-04-2025
# Versión del Python: 3.13.2
# Nombre del IDE donde se desarrolló el programa: Visual Studio Code
######################################################################################################################

from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import webbrowser

class Informacion(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()

    def widgets(self):
        self.configure(bg="#477296")  #Color de fondo

        # 🔹 Frame contenedor horizontal
        contenedor_horizontal = tk.Frame(self, bg="#477296")
        contenedor_horizontal.pack(expand=True, fill="both")

        # 🔹 Frame izquierdo (logo decorativo)
        frame_izquierdo = tk.Frame(contenedor_horizontal, bg="#477296")
        frame_izquierdo.pack(side="left", expand=True, fill="both")

        imagen_fondo = Image.open("imagenes/informacion.png").resize((500, 500))  # Cambiá ruta/size según tu imagen
        self.logo_fondo = ImageTk.PhotoImage(imagen_fondo)

        logo_label = tk.Label(frame_izquierdo, image=self.logo_fondo, bg="#477296")
        logo_label.pack(expand=True)

        # 🔸 Frame derecho (información de contacto)
        frame_derecho = tk.Frame(contenedor_horizontal, bg="#477296", width=400)
        frame_derecho.pack(side="right", expand=True)

        # 🔸 Sub-frame para centrar contenido
        contenido = tk.Frame(frame_derecho, bg="#477296")
        contenido.place(relx=0.5, rely=0.5, anchor="center")  # Centrado total


        titulo = tk.Label(frame_derecho, text="Información de contacto",
                          font=("Arial", 20, "bold"), bg="#477296", fg="white")
        titulo.pack(pady=10)

        imagen_pil = Image.open("iconos/butcher.png").resize((100, 100))
        self.imagen_tk_agregar = ImageTk.PhotoImage(imagen_pil)
        imagen_label = tk.Label(frame_derecho, image=self.imagen_tk_agregar, bg="#477296")
        imagen_label.pack(pady=5)

        descripcion = tk.Label(frame_derecho,
                               text="Contáctanos por WhatsApp al +506 8432-7296",
                               font=("Arial", 16), bg="#477296", fg="white")
        descripcion.pack(pady=10)

        boton = tk.Button(frame_derecho, text="Abrir WhatsApp",
                          command=lambda: webbrowser.open("https://api.whatsapp.com/send?phone=XXXXX-XXXXXX"),  # Reemplaza XXXXX-XXXXXX con el número real
                          font=("Arial", 16, "bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        boton.pack(pady=10)

