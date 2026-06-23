######################################################################################################################
# Nombre del programa: PROYECTO CARNICERIA.PY
# Nombres del programador: [Marcos Vargas Hernández]
# Fecha de elaboración del programa: 14-04-2025
# Versión del Python: 3.13.2
# Nombre del IDE donde se desarrolló el programa: Visual Studio Code
######################################################################################################################

# Importar módulos necesarios
import os  # Módulo para operaciones del sistema operativo
import sys  # Módulo para interactuar con el sistema
from tkinter import *  # Importar todos los elementos de Tkinter para la interfaz gráfica
from tkinter import ttk  # Importar ttk para estilos avanzados en Tkinter

"""
Este programa es una aplicación de gestión para una carnicería, que incluye funcionalidades de inicio de sesión y registro de usuarios.
El programa utiliza la biblioteca Tkinter para crear una interfaz gráfica de usuario (GUI) y está diseñado para ser modular, 
permitiendo la importación de diferentes módulos según sea necesario.
"""  

# Importar módulos adicionales con rutas dinámicas
try:
    from login import Login, Registro  # Importar clases Login y Registro desde el módulo login
    from container import Container  # Importar la clase Container desde el módulo container
except ImportError as e:
    # Si ocurre un error al importar, mostrar un mensaje y salir del programa
    print(f"Error al importar módulos: {e}")
    sys.exit(1)

# Definición de la clase principal de la aplicación
class Manager(Tk):  # Hereda de la clase Tk de Tkinter
    def __init__(self, *args, **kwargs):  # Constructor de la clase
        super().__init__(*args, **kwargs)  # Inicializar la clase base Tk
        self.title("Carnicería El Asadito V1.0")  # Título de la ventana
        self.geometry("1200x700+120+20")  # Tamaño y posición inicial de la ventana
        self.resizable(False, False)  # Deshabilitar el redimensionamiento de la ventana

        # Crear el contenedor principal
        container = Frame(self)  # Crear un frame que actuará como contenedor principal
        container.pack(side=TOP, fill=BOTH, expand=True)  # Configurar el contenedor para que ocupe todo el espacio
        container.configure(bg="#477296")  # Establecer el color de fondo del contenedor

        # Diccionario para almacenar los frames de la aplicación
        self.frames = {}

        # Crear y almacenar los frames definidos en la lista
        for FrameClass in (Login, Registro, Container):  # Iterar sobre las clases de frames
            try:
                # Crear una instancia del frame y almacenarla en el diccionario
                frame = FrameClass(container, self)
                self.frames[FrameClass] = frame
            except Exception as e:
                # Si ocurre un error al inicializar un frame, mostrar un mensaje
                print(f"Error al inicializar el frame {FrameClass.__name__}: {e}")

       
        self.show_frame(Login) # Mostrar el frame Container al iniciar la aplicación

        # Configurar el estilo de la interfaz gráfica
        self.style = ttk.Style()  # Crear un objeto Style para personalizar la apariencia
        self.style.theme_use("clam")  # Usar el tema "clam" para la interfaz

    def show_frame(self, container):  # Método para mostrar un frame específico
        """Muestra el frame solicitado."""
        frame = self.frames.get(container)  # Obtener el frame del diccionario
        if frame:
            frame.tkraise()  # Llevar el frame al frente
        else:
            # Si el frame no existe, mostrar una advertencia
            print(f"Advertencia: El frame {container.__name__} no existe.")

# Función principal para ejecutar la aplicación
def main():
    try:
        app = Manager()  # Crear una instancia de la clase Manager
        app.mainloop()  # Iniciar el bucle principal de la aplicación
    except Exception as e:
        # Si ocurre un error al ejecutar la aplicación, mostrar un mensaje
        print(f"Error al ejecutar la aplicación: {e}")

# Punto de entrada del programa
if __name__ == "__main__":
    main()  # Llamar a la función principal



