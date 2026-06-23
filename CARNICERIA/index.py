######################################################################################################################
# Nombre del programa: PROYECTO CARNICERIA.PY
# Nombres del programador: [Marcos Vargas Hernández]
# Fecha de elaboración del programa: 14-04-2025
# Versión del Python: 3.13.2
# Nombre del IDE donde se desarrolló el programa: Visual Studio Code
######################################################################################################################

"""
Este es el punto de entrada del programa. Aquí se inicializa la aplicación y se muestra la ventana principal.
El programa es una aplicación de gestión para una carnicería, que permite a los usuarios iniciar sesión, registrarse y gestionar productos.
"""

from manager import Manager  # Importar la clase Manager desde el módulo manager
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__": # Punto de entrada del programa
    app = Manager() # Crear una instancia de la clase Manager
    app.mainloop() # Iniciar el bucle principal de la aplicación

