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

import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry # importar el calendario
import sqlite3
from datetime import datetime
import os # importar el sistema operativo para crear carpetas
from reportlab.lib.pagesizes import letter    # importar el tamaño carta para reportes
from reportlab.lib import colors              # importar colores para el reporte
from reportlab.lib.units import inch          # importar unidades para el reporte
from reportlab.pdfgen import canvas           # importa la capacidad de crear PDF
from reportlab.pdfbase.ttfonts import TTFont  # importar la fuente TrueType
from reportlab.pdfbase import pdfmetrics       # importar la métrica de PDF
from PIL import Image, ImageTk # importar la biblioteca PIL para manejar imágenes

"""
Clase Caja: Esta clase representa la interfaz de la caja registradora y maneja las operaciones relacionadas con el arqueo de caja y 
la generación de informes de ventas.

"""


class Caja(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs) # Inicializar la clase Frame
        self.saldo = 0 # Inicializar el saldo a 0
        self.entradas = [] # Inicializar la lista de entradas
        self.salidas = [] # Inicializar la lista de salidas
        self.numero_informes = 1 # Inicializar el número de informes a 1
        self.productos_seleccionados = [] # Inicializar la lista de productos seleccionados

        # Ruta dinámica para la base de datos
        base_path = os.path.dirname(__file__)
        self.db_name = os.path.join(base_path, "database.db")

        # Ruta dinámica para la carpeta de informes
        self.informes_folder = os.path.join(base_path, "informes")
        os.makedirs(self.informes_folder, exist_ok=True)

        # Nueva línea para la carpeta de cierres de caja
        self.cierres_caja_folder = os.path.join(base_path, "cierres_caja")
        os.makedirs(self.cierres_caja_folder, exist_ok=True)

        self.widgets()

    def ver_ventas_realizadas(self): # Método para ver las ventas realizadas
        try:
            # Obtener las fechas seleccionadas
            fecha_inicio = self.dateentry_fecha1.get_date() # Obtener la fecha de inicio
            fecha_fin = self.dateentry_fecha2.get_date()
            print(f"Fecha inicio: {fecha_inicio}, Fecha fin: {fecha_fin}") # Imprimir las fechas seleccionadas

            # Validar que las fechas no sean nulas
            if not fecha_inicio or not fecha_fin:
                messagebox.showwarning("Advertencia", "Por favor, selecciona ambas fechas.")
                return

            # Conexión con la base de datos
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            print(f"Conectado a la base de datos: {self.db_name}")

            # Consulta con filtro de fechas
            query = "SELECT * FROM ventas WHERE fecha BETWEEN ? AND ?"
            parametros = (fecha_inicio.strftime('%d-%m-%Y'), fecha_fin.strftime('%d-%m-%Y'))
            print(f"Consulta: {query}, Parámetros: {parametros}")

            cursor.execute(query, parametros) # Ejecutar la consulta
            ventas = cursor.fetchall() # Obtener todas las ventas en el rango de fechas
            conn.close()
            #print(f"Ventas encontradas: {ventas}")

            # Limpiar el Treeview
            for item in self.tree.get_children(): # Eliminar todos los elementos del Treeview
                self.tree.delete(item)

            # Insertar datos en el Treeview
            self.productos_seleccionados = []  # Limpiar la lista antes de llenarla
            for venta in ventas:
                # Asegúrate de que los datos estén en el orden correcto
                self.tree.insert("", tk.END, values=(venta[0], venta[1], venta[2], venta[4], venta[5], venta[8])) # Agregar a la lista de productos seleccionados
                self.productos_seleccionados.append((venta[0], venta[1], venta[2], venta[4], venta[5], venta[8])) # Agregar a la lista de productos seleccionados

        except sqlite3.Error as e: 
            print(f"Error al ejecutar la consulta: {e}")
            messagebox.showerror("Error", f"Error al mostrar las ventas: {e}")
        
    def calcular_total_venta(self): # Calcular el total de ventas en el rango de fechas
        try:
            fecha_inicio = self.dateentry_fecha1.get_date().strftime('%d-%m-%Y') # Obtener la fecha de inicio
            fecha_fin = self.dateentry_fecha2.get_date().strftime('%d-%m-%Y') # Obtener la fecha de fin

            conn = sqlite3.connect(self.db_name) # Conectar a la base de datos
            cursor = conn.cursor()

            query = "SELECT SUM(total) FROM ventas WHERE fecha BETWEEN ? AND ?" # Consulta para obtener el total de ventas
            cursor.execute(query, (fecha_inicio, fecha_fin)) # Ejecutar la consulta
            # Obtener el resultado de la consulta
            total_venta = cursor.fetchone()[0]

            conn.close()

            return total_venta if total_venta else 0  # Si no hay ventas, devolver 0 
        except sqlite3.Error as e:
            messagebox.showerror(
                "Error", f"No se pudo calcular el total de ventas: {e}")
            return 0


    def generar_reporte_pdf(self, total_venta, fecha_inicio, fecha_fin): # Método para generar el informe de ventas PDF
        try:
            # Ruta del archivo PDF
            informes_path = os.path.join(self.informes_folder, f"Informes_{self.numero_informes}.pdf")
            c = canvas.Canvas(informes_path, pagesize=letter) # Crear un objeto canvas para el PDF

            # Información de la empresa
            empresa_nombre = "Carniceria El Asadito S.A"
            empresa_direccion = "San José, avenida 10, calle 3"
            empresa_telefono = "+506 2539-1088"
            empresa_email = "ventas@elasadito.com"
            empresa_website = "www.elasadito.com"

            # Encabezado del PDF
            c.setFont("Helvetica", 18)
            c.setFillColor(colors.darkblue)
            c.drawCentredString(300, 750, f"Informe de Ventas del {fecha_inicio.strftime('%d-%m-%Y')} al {fecha_fin.strftime('%d-%m-%Y')}")

            # Información de la empresa
            c.setFillColor(colors.black)
            c.setFont("Helvetica", 12)
            c.drawString(50, 710, f"{empresa_nombre}")
            c.drawString(50, 690, f"Dirección: {empresa_direccion}") # Dirección de la empresa
            c.drawString(50, 670, f"Teléfono: {empresa_telefono}")
            c.drawString(50, 650, f"Email: {empresa_email}")
            c.drawString(50, 630, f"Website: {empresa_website}")

            # Línea divisoria
            c.setLineWidth(0.5) # Establecer el grosor de la línea
            c.setStrokeColor(colors.gray) # Establecer el color de la línea
            c.line(50, 620, 550, 620) # Dibujar la línea divisoria

            # Información de la factura
            c.drawString(50, 600, f"Número de Informes: {self.numero_informes}") # Número de informes
            c.drawString(50, 580, f"Fecha: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}") # Fecha y hora actual

            # Tabla de productos
            y_offset = 540
            c.setFont("Helvetica", 11)
            c.drawString(60, y_offset, "Factura") # Encabezado de la tabla
            c.drawString(120, y_offset, "Cliente")
            c.drawString(180, y_offset, "Producto")
            c.drawString(350, y_offset, "Cantidad")
            c.drawString(420, y_offset, "Total")
            c.drawString(470, y_offset, "Fecha")
            c.line(50, y_offset - 10, 550, y_offset - 10)  # Línea divisoria
            y_offset -= 30

            # Agregar productos al PDF
            for item in self.productos_seleccionados:
                factura, cliente, producto, cantidad, total, fecha = item # Desempaquetar los datos de la venta
                c.drawString(60, y_offset, str(factura))  # Número de factura
                c.drawString(120, y_offset, str(cliente))
                c.drawString(180, y_offset, str(producto))
                c.drawString(350, y_offset, str(cantidad))
                c.drawString(420, y_offset, f"{total:,.0f}")
                c.drawString(470, y_offset, str(fecha))
                y_offset -= 20

                # Verificar si hay suficiente espacio en la página
                if y_offset < 50:
                    c.showPage()
                    y_offset = 750

            # Total de ventas
            c.setFont("Helvetica", 14)
            c.setFillColor(colors.darkblue)
            c.drawString(50, y_offset - 20, f"Total ventas del periodo:  {total_venta:,.0f}")

            # Guardar el PDF
            c.save()

            # Mostrar mensaje de éxito
            messagebox.showinfo("Informe Generado", f"Se ha generado el informe en: {informes_path}")

            # Abrir el archivo PDF
            os.startfile(os.path.abspath(informes_path))

            # Incrementar número de informes
            self.numero_informes += 1

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el informe: {e}")

    def widgets(self):
        # Ruta dinámica para los iconos
        base_path = os.path.dirname(__file__) # Obtener la ruta del directorio actual
        iconos_folder = os.path.join(base_path, "iconos") # Ruta de la carpeta de iconos

        # Verificar si el icono existe
        def cargar_icono(nombre): # Cargar icono desde la carpeta de iconos
            ruta_icono = os.path.join(iconos_folder, nombre) # Ruta del icono
            if os.path.exists(ruta_icono):
                imagen_pil = Image.open(ruta_icono)
                imagen_resize = imagen_pil.resize((30, 30))
                return ImageTk.PhotoImage(imagen_resize)
            else:
                print(f"Advertencia: No se encontró el icono {nombre}")
                return None

        # Marco principal
        labelframe = tk.LabelFrame(self, relief="raised", borderwidth=1, bg="#477296") # Crear un labelframe para la caja
        labelframe.place(x=25, y=30, width=1150, height=180)

        # Título del marco
        titulo_label = tk.Label(labelframe, text="Caja", font=("sans 16 bold"), bg="#477296", fg="white")
        titulo_label.place(x=10, y=10)

        # Fecha de inicio
        label_fecha1 = tk.Label(labelframe, text="Fecha Inicio: ", font=("sans 14 bold"), bg="#477296", fg="white")
        label_fecha1.place(x=10, y=50)

        self.dateentry_fecha1 = DateEntry(labelframe, width=12, date_pattern='dd-MM-yyyy', background='darkblue', foreground='white', borderwidth=2)
        self.dateentry_fecha1.place(x=20, y=90, width=100, height=30)

        # Fecha de fin
        label_fecha2 = tk.Label(labelframe, text="Fecha Fin:", font=("sans 14 bold"), bg="#477296", fg="white")
        label_fecha2.place(x=200, y=50)

        self.dateentry_fecha2 = DateEntry(labelframe, width=12, date_pattern='dd-MM-yyyy', background='darkblue', foreground='white', borderwidth=2)
        self.dateentry_fecha2.place(x=200, y=90, width=100, height=30)

        # Botón para filtrar por fecha
        btn_filtrar_fecha = tk.Button(labelframe, text="Filtrar", bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296", font="sans 12 bold", command=self.ver_ventas_realizadas)
        btn_filtrar_fecha.place(x=350, y=90, width=150, height=40)

        # Cargar icono para el botón de imprimir
        imagen_tk_imprimir_pdf = cargar_icono("imprimir.png")

        # Botón para imprimir a PDF
        btn_imprimir_pdf = tk.Button(labelframe, text="Imprimir PDF", bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296", font="sans 12 bold",
                                     command=lambda: self.generar_reporte_pdf(self.calcular_total_venta(), self.dateentry_fecha1.get_date(), self.dateentry_fecha2.get_date()))
        if imagen_tk_imprimir_pdf:
            btn_imprimir_pdf.config(image=imagen_tk_imprimir_pdf, compound=LEFT)
            btn_imprimir_pdf.image = imagen_tk_imprimir_pdf  # Mantener una referencia a la imagen
        btn_imprimir_pdf.place(x=550, y=90, width=150, height=40)

        # Crear frame para Treeview
        treFrame = tk.Frame(self, bg="white") 
        treFrame.place(x=70, y=220, width=1050, height=300) 

        # Scrollbars
        scrol_y = ttk.Scrollbar(treFrame) # Crear scrollbar vertical
        scrol_y.pack(side=RIGHT, fill=Y) # Llenar el scrollbar vertical
        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL) # Crear scrollbar horizontal
        scrol_x.pack(side=BOTTOM, fill=X) # Llenar el scrollbar horizontal

        # Configuración del Treeview
        self.tree = ttk.Treeview(treFrame, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, height=40, columns=(
            "Factura", "Cliente", "Producto", "Cantidad", "Total", "Fecha"), show="headings") # Mostrar encabezados
        self.tree.pack(expand=TRUE, fill=BOTH)

        # Configuración de columnas
        self.tree.heading("Factura", text="Factura")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Producto", text="Producto")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Total", text="Total")
        self.tree.heading("Fecha", text="Fecha")  # Encabezado para la columna de fecha

        # Configuración de las columnas
        self.tree.column("Factura", width=30, anchor="center")
        self.tree.column("Cliente", width=100, anchor="center")
        self.tree.column("Producto", width=170, anchor="center")
        self.tree.column("Cantidad", width=60, anchor="center")
        self.tree.column("Total", width=60, anchor="center")
        self.tree.column("Fecha", width=80, anchor="center")  # Ajusta el ancho si es necesario

        # Configuración de los scrollbars
        scrol_y.config(command=self.tree.yview) # Configurar el scrollbar vertical
        scrol_x.config(command=self.tree.xview) # Configurar el scrollbar horizontal

        # Cargar icono para el botón de arqueo
        imagen_tk_arqueo = cargar_icono("arqueo.png")

        # Botón para Arqueo
        boton_arqueo = tk.Button(self, text="Arqueo", bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296", font="sans 12 bold", command=lambda: self.arqueo())
        if imagen_tk_arqueo: # Verificar si la imagen se cargó correctamente
            boton_arqueo.config(image=imagen_tk_arqueo, compound=LEFT)
            boton_arqueo.image = imagen_tk_arqueo
        boton_arqueo.place(x=800, y=120, width=150, height=40) # Botón para arqueo

    # Métodos para calcular el total de monedas
    def calcular_total_monedas_5(self, event=None): # Método para calcular el total de monedas de 5
        try:
            cantidad_monedas_5 = int(self.label_moneda_5.get() or 0)  # Usa 0 si el campo está vacío
            total_monedas_5 = cantidad_monedas_5 * 5  # Calcular el total de monedas de 5
            resultado_formateado = f"₵ {total_monedas_5:,.0f}" # Formatear el resultado
            self.label_cantidad_5.delete(0, tk.END) # Limpiar el campo de cantidad
            self.label_cantidad_5.insert(0, resultado_formateado) # Insertar el resultado formateado
            self.sumatoria_total()  # Llama a sumatoria_total después de actualizar
        except ValueError:
            self.label_cantidad_5.delete(0, tk.END)

    def calcular_total_monedas_10(self, event=None):  # Método para calcular el total de monedas de 10
        try:
            cantidad_monedas_10 = int(self.label_moneda_10.get() or 0)
            total_monedas_10 = cantidad_monedas_10 * 10
            resultado_formateado = f"₵ {total_monedas_10:,.0f}"
            self.label_cantidad_10.delete(0, tk.END)
            self.label_cantidad_10.insert(0, resultado_formateado)
            self.sumatoria_total()
        except ValueError:
            self.label_cantidad_10.delete(0, tk.END)

    def calcular_total_monedas_25(self, event=None): # Método para calcular el total de monedas de 25
        try:
            cantidad_monedas_25 = int(self.label_moneda_25.get() or 0)
            total_monedas_25 = cantidad_monedas_25 * 25
            resultado_formateado = f"₵ {total_monedas_25:,.0f}"
            self.label_cantidad_25.delete(0, tk.END)
            self.label_cantidad_25.insert(0, resultado_formateado)
            self.sumatoria_total()
        except ValueError:
            self.label_cantidad_25.delete(0, tk.END)

    def calcular_total_monedas_50(self, event=None): # Método para calcular el total de monedas de 50
        try:
            cantidad_monedas_50 = int(self.label_moneda_50.get() or 0)
            total_monedas_50 = cantidad_monedas_50 * 50
            resultado_formateado = f"₵ {total_monedas_50:,.0f}"
            self.label_cantidad_50.delete(0, tk.END)
            self.label_cantidad_50.insert(0, resultado_formateado)
            self.sumatoria_total()
        except ValueError:
            self.label_cantidad_50.delete(0, tk.END)

    def calcular_total_monedas_100(self, event=None): # Método para calcular el total de monedas de 100
        try:
            cantidad_monedas_100 = int(self.label_moneda_100.get() or 0)
            total_monedas_100 = cantidad_monedas_100 * 100
            resultado_formateado = f"₵ {total_monedas_100:,.0f}"
            self.label_cantidad_100.delete(0, tk.END)
            self.label_cantidad_100.insert(0, resultado_formateado)
            self.sumatoria_total()
        except ValueError:
            self.label_cantidad_100.delete(0, tk.END)

    def calcular_total_monedas_500(self, event=None):   # Método para calcular el total de monedas de 500
        try:
            cantidad_monedas_500 = int(self.label_moneda_500.get() or 0)
            total_monedas_500 = cantidad_monedas_500 * 500
            resultado_formateado = f"₵ {total_monedas_500:,.0f}"
            self.label_cantidad_500.delete(0, tk.END)
            self.label_cantidad_500.insert(0, resultado_formateado)
            self.sumatoria_total()
        except ValueError:
            self.label_cantidad_500.delete(0, tk.END)

    # Métodos para calcular el total de billetes
    def calcular_total_billetes_1000(self, event=None): # Método para calcular el total de billetes de 1000
        try:
            cantidad_billetes_1000 = int(self.label_billete_1000.get() or 0)
            total_billetes_1000 = cantidad_billetes_1000 * 1000
            resultado_formateado = f"₵ {total_billetes_1000:,.0f}"
            self.label_cantidad_1000.delete(0, tk.END)
            self.label_cantidad_1000.insert(0, resultado_formateado)
            self.sumatoria_total()
        except ValueError:
            self.label_cantidad_1000.delete(0, tk.END)

    def calcular_total_billetes_2000(self, event=None): # Método para calcular el total de billetes de 2000 
        try:
            cantidad_billetes_2000 = int(self.label_billete_2000.get() or 0)
            total_billetes_2000 = cantidad_billetes_2000 * 2000
            resultado_formateado = f"₵ {total_billetes_2000:,.0f}"
            self.label_cantidad_2000.delete(0, tk.END)
            self.label_cantidad_2000.insert(0, resultado_formateado)
            self.sumatoria_total()
        except ValueError:
            self.label_cantidad_2000.delete(0, tk.END)

    def calcular_total_billetes_5000(self, event=None): # Método para calcular el total de billetes de 5000
        try:
            cantidad_billetes_5000 = int(self.label_billete_5000.get() or 0)
            total_billetes_5000 = cantidad_billetes_5000 * 5000
            resultado_formateado = f"₵ {total_billetes_5000:,.0f}"
            self.label_cantidad_5000.delete(0, tk.END)
            self.label_cantidad_5000.insert(0, resultado_formateado)
            self.sumatoria_total()
        except ValueError:
            self.label_cantidad_5000.delete(0, tk.END)

    def calcular_total_billetes_10000(self, event=None): # Método para calcular el total de billetes de 10.000
        try:
            cantidad_billetes_10000 = int(self.label_billete_10000.get() or 0)
            total_billetes_10000 = cantidad_billetes_10000 * 10000
            resultado_formateado = f"₵ {total_billetes_10000:,.0f}"
            self.label_cantidad_10000.delete(0, tk.END)
            self.label_cantidad_10000.insert(0, resultado_formateado)
            self.sumatoria_total()
        except ValueError:
            self.label_cantidad_10000.delete(0, tk.END)

    def calcular_total_billetes_20000(self, event=None): # Método para calcular el total de billetes de 20.000
        try:
            cantidad_billetes_20000 = int(self.label_billete_20000.get() or 0)
            total_billetes_20000 = cantidad_billetes_20000 * 20000
            resultado_formateado = f"₵ {total_billetes_20000:,.0f}"
            self.label_cantidad_20000.delete(0, tk.END)
            self.label_cantidad_20000.insert(0, resultado_formateado)
            self.sumatoria_total()
        except ValueError:
            self.label_cantidad_20000.delete(0, tk.END)

    def formatear_sinpe(self, event=None): # Método para formatear el campo de Sinpe Móvil
        try:
            # Obtener el valor ingresado en Sinpe Móvil
            texto_sinpe = self.label_cantidad_sinpe.get().replace("₵", "").replace(",", "").strip() # Limpiar el texto
            cantidad_sinpe = int(texto_sinpe)  # Convertir a entero
            # Formatear el resultado con ₵ :,.0f
            resultado_formateado = f"₵ {cantidad_sinpe:,.0f}"
            # Mostrar el resultado formateado en el mismo campo
            self.label_cantidad_sinpe.delete(0, tk.END)
            self.label_cantidad_sinpe.insert(0, resultado_formateado)
        except ValueError:
            # Si el campo está vacío o no es un número válido, limpiar el campo
            self.label_cantidad_sinpe.delete(0, tk.END)

    def formatear_tarjeta(self, event=None): # Método para formatear el campo de Tarjeta
        try:
            # Obtener el valor ingresado en Tarjeta
            texto_tarjeta = self.label_cantidad_tarjeta.get().replace("₵", "").replace(",", "").strip()
            cantidad_tarjeta = int(texto_tarjeta)  # Convertir a entero
            # Formatear el resultado con ₵ :,.0f
            resultado_formateado = f"₵ {cantidad_tarjeta:,.0f}"
            # Mostrar el resultado formateado en el mismo campo
            self.label_cantidad_tarjeta.delete(0, tk.END)
            self.label_cantidad_tarjeta.insert(0, resultado_formateado)
        except ValueError:
            # Si el campo está vacío o no es un número válido, limpiar el campo
            self.label_cantidad_tarjeta.delete(0, tk.END)

    def sumatoria_total(self, event=None):  # Agregar event para manejar el evento <KeyRelease>
        try:
            # Obtener los valores de las entradas
            saldo_inicial = float(self.saldo_inicial.get() or 0)
            total_monedas_5 = float(self.label_cantidad_5.get().replace("₵", "").replace(",", "").strip() or 0)
            total_monedas_10 = float(self.label_cantidad_10.get().replace("₵", "").replace(",", "").strip() or 0)
            total_monedas_25 = float(self.label_cantidad_25.get().replace("₵", "").replace(",", "").strip() or 0)
            total_monedas_50 = float(self.label_cantidad_50.get().replace("₵", "").replace(",", "").strip() or 0)
            total_monedas_100 = float(self.label_cantidad_100.get().replace("₵", "").replace(",", "").strip() or 0)
            total_monedas_500 = float(self.label_cantidad_500.get().replace("₵", "").replace(",", "").strip() or 0)
            total_billetes_1000 = float(self.label_cantidad_1000.get().replace("₵", "").replace(",", "").strip() or 0)
            total_billetes_2000 = float(self.label_cantidad_2000.get().replace("₵", "").replace(",", "").strip() or 0)
            total_billetes_5000 = float(self.label_cantidad_5000.get().replace("₵", "").replace(",", "").strip() or 0)
            total_billetes_10000 = float(self.label_cantidad_10000.get().replace("₵", "").replace(",", "").strip() or 0)
            total_billetes_20000 = float(self.label_cantidad_20000.get().replace("₵", "").replace(",", "").strip() or 0)
            total_sinpe = float(self.label_cantidad_sinpe.get().replace("₵", "").replace(",", "").strip() or 0)
            total_tarjeta = float(self.label_cantidad_tarjeta.get().replace("₵", "").replace(",", "").strip() or 0)

            # Calcular la sumatoria
            total = (total_monedas_5 + total_monedas_10 + total_monedas_25 + total_monedas_50 + \
                    total_monedas_100 + total_monedas_500 + total_billetes_1000 + total_billetes_2000 + \
                    total_billetes_5000 + total_billetes_10000 + total_billetes_20000 + total_sinpe + total_tarjeta) - saldo_inicial

            # Formatear el resultado y mostrarlo en self.label_total
            resultado_formateado = f"₵ {total:,.0f}"
            self.label_total_caja.delete(0, tk.END)
            self.label_total_caja.insert(0, resultado_formateado)

        except ValueError:
            # Si ocurre un error, limpiar el campo
            self.label_total_caja.delete(0, tk.END)

    def arqueo(self): # Método para realizar el arqueo de caja
        # Crear una nueva ventana para el arqueo
        arqueo_caja = tk.Toplevel(self)
        arqueo_caja.title("Arqueo de Caja")
        arqueo_caja.geometry("1100x750+120+20")
        arqueo_caja.config(bg="#477296")
        arqueo_caja.resizable(False, False)
        arqueo_caja.transient(self.master)  # Mantener la ventana como hija de la ventana principal
        arqueo_caja.grab_set() # Deshabilitar la ventana principal mientras está abierta
        arqueo_caja.focus_set() # Focalizar la ventana de arqueo
        arqueo_caja.lift() # Llevar la ventana al frente

        # creacion del labelframe  para datos iniciales
        label_1 = tk.Label(arqueo_caja, text="Arqueo Carnicería el Asadito", font="sans 16 bold", bg="#477296", fg="white")
        label_1.pack(pady=10)

        # Llamar a las funciones para crear los LabelFrame
        self.labelframe_1(arqueo_caja) 
        self.labelframe_2(arqueo_caja)
        self.labelframe_3(arqueo_caja)
        self.labelframe_4(arqueo_caja)
        self.labelframe_5(arqueo_caja)
        

        #============= 1 label frame =====================================###
    def labelframe_1(self, arqueo_caja): # LabelFrame donde esta la fecha y el saldo inicial
        labelframe = tk.LabelFrame(arqueo_caja, relief="raised", borderwidth=1, bg="#477296") ## Crear un labelframe para el arqueo
        labelframe.place(x=10, y=45, width=1050, height=95)

        # Se elije automaticamente la fecha del día para el arqueo
        fecha_hoy = datetime.now().strftime('%d-%m-%Y')
        label_fecha = tk.Label(labelframe, text=f"Fecha: {fecha_hoy}",font="sans 14 bold", bg="#477296", fg="white", anchor="w")
        label_fecha.place(x=150, y=20, width=180, height=30)

        # Label para el saldo inicial
        label_saldo_inicial = tk.Label(labelframe, text="Saldo Inicial ₵: ", font=("sans 14 bold"), bg="#477296", fg="white", anchor="w")
        label_saldo_inicial.place(x=390, y=20, width=150, height=30) 

        self.saldo_inicial = tk.Entry(labelframe, font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")  
        self.saldo_inicial.place(x=540, y=20, width=150, height=30)  
        self.saldo_inicial.bind("<KeyRelease>", self.sumatoria_total) # Vincula el evento <KeyRelease> al campo de entrada

        
    def calcular_ventas_dia(self):  # Método para calcular las ventas del día
        fecha_seleccionada = self.dateentry_fecha_informe.get_date().strftime('%d-%m-%Y')
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            query = "SELECT SUM(total) FROM ventas WHERE fecha = ?"
            cursor.execute(query, (fecha_seleccionada,))
            total_ventas = cursor.fetchone()[0]
            conn.close()

            # Mostrar el total de ventas en el Entry
            total_ventas = total_ventas if total_ventas else 0
            self.label_total_ventas_dia.config(state="normal")
            self.label_total_ventas_dia.delete(0, tk.END)
            self.label_total_ventas_dia.insert(0, f"₵ {total_ventas:,.0f}")
            self.label_total_ventas_dia.config(state="readonly")
        except sqlite3.Error as e:
            messagebox.showerror(
                "Error", f"No se pudo calcular las ventas del día: {e}")
                
        

    def labelframe_2(self, arqueo_caja): # LabelFrame donde estan las denominaciones de monedas y billetes, se ingresan cantidades y se calcula el total

        #Label para descripciones del arqueo
        label_descripcion = tk.LabelFrame(arqueo_caja, relief="raised", borderwidth=1, font=("sans 10"), bg="#477296", fg="black")    
        label_descripcion.place(x=10, y=145, width=285, height=450)

        label_descripcion1 = tk.Label(arqueo_caja, text="Descripción ", relief="solid",bd=2, font=("sans 12 bold"), bg="#477296", fg="white")
        label_descripcion1.place(x=25, y=150, width=255, height=30)

        #========= Creación de etiquetas en el labelframe de descripción para monedas ==============================================================#
        # Etiqueta monedas de 5
        label_moneda_5 = tk.Label(label_descripcion, text="Monedas de ₵ 5:", font=("sans 12 bold"), bg="#477296", fg="white", anchor="w")
        label_moneda_5.place(x=10, y=45, width=200, height=20)
        self.label_moneda_5 = tk.Entry(label_descripcion, font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        self.label_moneda_5.place(x=190, y=45, width=75, height=20)

        # Vincular el evento <KeyRelease> al campo de entrada de monedas de ₵5
        self.label_moneda_5.bind("<KeyRelease>", self.calcular_total_monedas_5)
    
        # Etiquetas monedas de 10
        label_moneda_10 = tk.Label(label_descripcion, text="Monedas de ₵ 10:", font=("sans 12 bold"), bg="#477296", fg="white", anchor="w")
        label_moneda_10.place(x=10, y=75, width=200, height=20)
        self.label_moneda_10 = tk.Entry(label_descripcion, font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        self.label_moneda_10.place(x=190, y=75, width=75, height=20)

        # Vincular el evento <KeyRelease> al campo de entrada de monedas de ₵10
        self.label_moneda_10.bind("<KeyRelease>", self.calcular_total_monedas_10)
    
        # Etiquetas monedas de 25
        label_moneda_25 = tk.Label(label_descripcion, text="Monedas de ₵ 25:", font=("sans 12 bold"), bg="#477296", fg="white", anchor="w")
        label_moneda_25.place(x=10, y=105, width=200, height=20)
        self.label_moneda_25 = tk.Entry(label_descripcion, bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        self.label_moneda_25.place(x=190, y=105, width=75, height=20)

        # Vincular el evento <KeyRelease> al campo de entrada de monedas de ₵25
        self.label_moneda_25.bind("<KeyRelease>", self.calcular_total_monedas_25)
    
        # Etiquetas monedas de 50
        label_moneda_50 = tk.Label(label_descripcion, text="Monedas de ₵ 50: ", font=("sans 12 bold"), bg="#477296", fg="white", anchor="w")
        label_moneda_50.place(x=10, y=135, width=200, height=20)
        self.label_moneda_50 = tk.Entry(label_descripcion, font=("sans 12 bold"),bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        self.label_moneda_50.place(x=190, y=135, width=75, height=20)

        # Vincular el evento <KeyRelease> al campo de entrada de monedas de ₵50
        self.label_moneda_50.bind("<KeyRelease>", self.calcular_total_monedas_50)
    
        # Etiquetas monedas de 100
        label_moneda_100 = tk.Label(label_descripcion, text="Monedas de ₵ 100:", font=("sans 12 bold"), bg="#477296", fg="white", anchor="w")
        label_moneda_100.place(x=10, y=165, width=200, height=20)
        self.label_moneda_100 = tk.Entry(label_descripcion, font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        self.label_moneda_100.place(x=190, y=165, width=75, height=20)

        # Vincular el evento <KeyRelease> al campo de entrada de monedas de ₵100
        self.label_moneda_100.bind("<KeyRelease>", self.calcular_total_monedas_100)
    
        # Etiquetas monedas de 500
        label_moneda_500 = tk.Label(label_descripcion, text="Monedas de ₵ 500:", font=("sans 12 bold"), bg="#477296", fg="white", anchor="w")
        label_moneda_500.place(x=10, y=195, width=200, height=20)
        self.label_moneda_500 = tk.Entry(label_descripcion, font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        self.label_moneda_500.place(x=190, y=195, width=75, height=20)

        # Vincular el evento <KeyRelease> al campo de entrada de monedas de ₵500
        self.label_moneda_500.bind("<KeyRelease>", self.calcular_total_monedas_500)
    
        # =============== Creación de etiquetas en el labelframe de descripción para billetes ===============
        # Etiquetas billetes de 1.000
        label_billete_1000 = tk.Label(label_descripcion, text="Billetes de ₵ 1.000:", font=("sans 12 bold"), bg="#477296", fg="white", anchor="w")
        label_billete_1000.place(x=10, y=225, width=200, height=20)
        self.label_billete_1000 = tk.Entry(label_descripcion, font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        self.label_billete_1000.place(x=190, y=225, width=75, height=20)

        # Vincular el evento <KeyRelease> al campo de entrada de monedas de ₵1000
        self.label_billete_1000.bind("<KeyRelease>", self.calcular_total_billetes_1000)
        
        # Etiquetas billetes de 2.000
        label_billete_2000 = tk.Label(label_descripcion, text="Billetes de ₵ 2.000:", font=("sans 12 bold"), bg="#477296", fg="white", anchor="w")
        label_billete_2000.place(x=10, y=255, width=200, height=20)
        self.label_billete_2000 = tk.Entry(label_descripcion, font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        self.label_billete_2000.place(x=190, y=255, width=75, height=20)

        # Vincular el evento <KeyRelease> al campo de entrada de monedas de ₵2.000
        self.label_billete_2000.bind("<KeyRelease>", self.calcular_total_billetes_2000)
        
        #Etiquetas billetes de 5.000
        label_billete_5000 = tk.Label(label_descripcion, text="Billetes de ₵ 5.000:", font=("sans 12 bold"), bg="#477296", fg="white", anchor="w")
        label_billete_5000.place(x=10, y=285, width=200, height=20)
        self.label_billete_5000= tk.Entry(label_descripcion, font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        self.label_billete_5000.place(x=190, y=285, width=75, height=20)

        # Vincular el evento <KeyRelease> al campo de entrada de monedas de ₵5.000
        self.label_billete_5000.bind("<KeyRelease>", self.calcular_total_billetes_5000)
        
        # Etiquetas billetes de 10.000
        label_billete_10000 = tk.Label(label_descripcion, text="Billetes de ₵ 10.000:", font=("sans 12 bold"), bg="#477296", fg="white", anchor="w")
        label_billete_10000.place(x=10, y=315, width=200, height=20)
        self.label_billete_10000 = tk.Entry(label_descripcion, font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        self.label_billete_10000.place(x=190, y=315, width=75, height=20)

        # Vincular el evento <KeyRelease> al campo de entrada de monedas de ₵10.000
        self.label_billete_10000.bind("<KeyRelease>", self.calcular_total_billetes_10000)
    
        # Etiquetas billetes de 20.000
        label_billete_20000 = tk.Label(label_descripcion, text="Billetes de ₵ 20.000:", font=("sans 12 bold"), bg="#477296", fg="white", anchor="w")
        label_billete_20000.place(x=10, y=345, width=200, height=20)
        self.label_billete_20000= tk.Entry(label_descripcion, font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        self.label_billete_20000.place(x=190, y=345, width=75, height=20)

        # Vincular el evento <KeyRelease> al campo de entrada de monedas de ₵20.000
        self.label_billete_20000.bind("<KeyRelease>", self.calcular_total_billetes_20000)
        
        # Pagos por sinpe Movil
        label_sinpe = tk.Label(label_descripcion, text="Recibido por Sinpe Móvil:", font=("sans 12 bold"), bg="#477296", fg="white", anchor="w")
        label_sinpe.place(x=10, y=375, width=250, height=20)

        # Pagos con tarjeta
        label_tarjeta = tk.Label(label_descripcion, text="Recibido por Tarjeta:", font=("sans 12 bold"), bg="#477296", fg="white", anchor="w")
        label_tarjeta.place(x=10, y=405, width=250, height=20)
        
    def labelframe_3(self, arqueo_caja): # LabelFrame donde se realizan detallan la cantidad de dinero según el tipo de moneda o billete
        ## ================================= CREACION DEL 2 LABEL FRAME PARA CONTAR DINERO ====================================##
        # Label para contar dinero
        label_descripcion2 = tk.LabelFrame(arqueo_caja, relief="raised", borderwidth=1, font=("sans 10"), bg="#477296", fg="black")
        label_descripcion2.place(x=300, y=145, width=350, height=450)

        label_descrip_2 = tk.Label(label_descripcion2, text="Cantidad por Denominación ", relief="solid", bd=2, font=("sans 12 bold"), bg="#477296", fg="white")
        label_descrip_2.place(x=10, y=5, width=330, height=30)

        # Cantidad de monedas de 5
        label_cantidad_5 = tk.Label(label_descripcion2, text="Cantidad de ₵ 5:", font=("sans 12 bold"), bg="#477296", fg="white", anchor="w")
        label_cantidad_5.place(x=10, y=45, width=200, height=20)
        self.label_cantidad_5 = tk.Entry(label_descripcion2, font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        self.label_cantidad_5.place(x=190, y=45, width=150, height=20)
        self.label_cantidad_5.bind("<KeyRelease>", self.sumatoria_total) # Vincula el evento <KeyRelease> al campo de cantidad

        # Cantidad de monedas de 10
        label_cantidad_10 = tk.Label(label_descripcion2, text="Cantidad de ₵ 10:", font=("sans 12 bold"), bg="#477296", fg="white", anchor="w")
        label_cantidad_10.place(x=10, y=75, width=200, height=20)
        self.label_cantidad_10 = tk.Entry(label_descripcion2, font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        self.label_cantidad_10.place(x=190, y=75, width=150, height=20)
        self.label_cantidad_10.bind("<KeyRelease>", self.sumatoria_total)

        # Cantidad de monedas de 25
        label_cantidad_25 = tk.Label(label_descripcion2, text="Cantidad de ₵ 25:", font=("sans 12 bold"), bg="#477296", fg="white", anchor="w")
        label_cantidad_25.place(x=10, y=105, width=200, height=20)
        self.label_cantidad_25 = tk.Entry(label_descripcion2, font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        self.label_cantidad_25.place(x=190, y=105, width=150, height=20)
        self.label_cantidad_25.bind("<KeyRelease>", self.sumatoria_total)

        # Cantidad de monedas de 50
        label_cantidad_50 = tk.Label(label_descripcion2, text="Cantidad de ₵ 50:", font=("sans 12 bold"), bg="#477296", fg="white", anchor="w")
        label_cantidad_50.place(x=10, y=135, width=200, height=20)
        self.label_cantidad_50 = tk.Entry(label_descripcion2, font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        self.label_cantidad_50.place(x=190, y=135, width=150, height=20)
        self.label_cantidad_50.bind("<KeyRelease>", self.sumatoria_total)

        # Cantidad de monedas de 100
        label_cantidad_100 = tk.Label(label_descripcion2, text="Cantidad de ₵ 100:", font=("sans 12 bold"), bg="#477296", fg="white", anchor="w")
        label_cantidad_100.place(x=10, y=165, width=200, height=20)
        self.label_cantidad_100 = tk.Entry(label_descripcion2, font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        self.label_cantidad_100.place(x=190, y=165, width=150, height=20)
        self.label_cantidad_100.bind("<KeyRelease>", self.sumatoria_total)

        # Cantidad de monedas de 500
        label_cantidad_500 = tk.Label(label_descripcion2, text="Cantidad de ₵ 500:", font=("sans 12 bold"), bg="#477296", fg="white", anchor="w")
        label_cantidad_500.place(x=10, y=195, width=200, height=20)
        self.label_cantidad_500 = tk.Entry(label_descripcion2, font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        self.label_cantidad_500.place(x=190, y=195, width=150, height=20)
        self.label_cantidad_500.bind("<KeyRelease>", self.sumatoria_total)

        # Cantidad de billetes de 1.000
        label_cantidad_1000 = tk.Label(label_descripcion2, text="Cantidad de ₵ 1.000:", font=("sans 12 bold"), bg="#477296", fg="white", anchor="w")
        label_cantidad_1000.place(x=10, y=225, width=200, height=20)
        self.label_cantidad_1000 = tk.Entry(label_descripcion2, font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        self.label_cantidad_1000.place(x=190, y=225, width=150, height=20)
        self.label_cantidad_1000.bind("<KeyRelease>", self.sumatoria_total)

        # Cantidad de billetes de 2.000
        label_cantidad_2000 = tk.Label(label_descripcion2, text="Cantidad de ₵ 2.000:", font=("sans 12 bold"), bg="#477296", fg="white", anchor="w")
        label_cantidad_2000.place(x=10, y=255, width=200, height=20)
        self.label_cantidad_2000 = tk.Entry(label_descripcion2, font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        self.label_cantidad_2000.place(x=190, y=255, width=150, height=20)
        self.label_cantidad_2000.bind("<KeyRelease>", self.sumatoria_total)

        # Cantidad de billetes de 5.000
        label_cantidad_5000 = tk.Label(label_descripcion2, text="Cantidad de ₵ 5.000:", font=("sans 12 bold"), bg="#477296", fg="white", anchor="w")
        label_cantidad_5000.place(x=10, y=285, width=200, height=20)
        self.label_cantidad_5000 = tk.Entry(label_descripcion2, font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        self.label_cantidad_5000.place(x=190, y=285, width=150, height=20)
        self.label_cantidad_5000.bind("<KeyRelease>", self.sumatoria_total)

        # Cantidad de billetes de 10.000
        label_cantidad_10000 = tk.Label(label_descripcion2, text="Cantidad de ₵ 10.000:", font=("sans 12 bold"), bg="#477296", fg="white", anchor="w")
        label_cantidad_10000.place(x=10, y=315, width=200, height=20)
        self.label_cantidad_10000 = tk.Entry(label_descripcion2, font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        self.label_cantidad_10000.place(x=190, y=315, width=150, height=20)
        self.label_cantidad_10000.bind("<KeyRelease>", self.sumatoria_total)

        # Cantidad de billetes de 20.000
        label_cantidad_20000 = tk.Label(label_descripcion2, text="Cantidad de ₵ 20.000:", font=("sans 12 bold"), bg="#477296", fg="white", anchor="w")
        label_cantidad_20000.place(x=10, y=345, width=200, height=20)
        self.label_cantidad_20000 = tk.Entry(label_descripcion2, font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        self.label_cantidad_20000.place(x=190, y=345, width=150, height=20)
        self.label_cantidad_20000.bind("<KeyRelease>", self.sumatoria_total)

        # Cantidad de pagos por sinpe móvil
        label_cantidad_sinpe = tk.Label(label_descripcion2, text="Cantidad por Sinpe:", font=("sans 12 bold"), bg="#477296", fg="white", anchor="w")
        label_cantidad_sinpe.place(x=10, y=375, width=200, height=20)
        self.label_cantidad_sinpe = tk.Entry(label_descripcion2, font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        self.label_cantidad_sinpe.place(x=190, y=375, width=150, height=20)
        self.label_cantidad_sinpe.bind("<KeyRelease>", self.sumatoria_total)

        # Cantidad de pagos por tarjeta
        label_cantidad_tarjeta = tk.Label(label_descripcion2, text="Cantidad por Tarjeta:", font=("sans 12 bold"), bg="#477296", fg="white", anchor="w")
        label_cantidad_tarjeta.place(x=10, y=405, width=200, height=20)
        self.label_cantidad_tarjeta = tk.Entry(label_descripcion2, font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        self.label_cantidad_tarjeta.place(x=190, y=405, width=150, height=20)
        self.label_cantidad_tarjeta.bind("<KeyRelease>", self.sumatoria_total)
        
    def labelframe_4(self, arqueo_caja): # LabelFrame donde se totaliza el dinero
        ## ==================================CREACION DEL 4 LABELFRAME PARA TOTALIZAR DINERO ====================================##
        # Label para totalizar dinero
        label_total = tk.LabelFrame(arqueo_caja, relief="raised", borderwidth=1, font=("sans 10"), bg="#477296", fg="black")
        label_total.place(x=10, y=600, width=1050, height=100)

        label_total_caja = tk.Label(label_total, text="Dinero Total en Caja:", relief="solid", bd=2, font=("sans 12 bold"), bg="#477296", fg="white")
        label_total_caja.place(x=150, y=5, width=250, height=30)

        # Label para sumatoria total del dinero realizado en el día
        self.label_total_caja = tk.Entry(label_total, font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        self.label_total_caja.place(x=430, y=5, width=200, height=30)
            
###########################################################################################################################################3
    def labelframe_5(self, arqueo_caja): # LabelFrame donde se realizan los reportes de cierre de caja
        ## ==================================CREACION DEL 5 LABELFRAME PARA BOTONES DE ACCION ====================================##
        # Label para botones de acción
        label_reportes = tk.LabelFrame(arqueo_caja, relief="raised", borderwidth=1, font=("sans 10"), bg="#477296", fg="black")
        label_reportes.place(x=655, y=145, width=405, height=450)

        label_cierres = tk.Label(label_reportes, text="Cierre de caja", relief="solid", bd=2, font=("sans 12 bold"), bg="#477296", fg="white")
        label_cierres.place(x=10, y=5, width=385, height=30)

        #Label para seleccionar la fecha del informe de ventas
        label_fecha_informe = tk.Label(label_reportes, text="Fecha de Ventas:", font=("sans 12 bold"), bg="#477296", fg="white")
        label_fecha_informe.place(x=10, y=50, width=140, height=30)

        # DateEntry para seleccionar la fecha
        self.dateentry_fecha_informe = DateEntry(label_reportes, width=12, date_pattern='dd-MM-yyyy', background='darkblue', foreground='white', borderwidth=2)
        self.dateentry_fecha_informe.place(x=155, y=50, width=100, height=30)

        # Label para mostrar el total de ventas del día
        label_ventas_dia = tk.Label(label_reportes, text="Ventas del Día:", font=("sans 12 bold"), bg="#477296", fg="white")
        label_ventas_dia.place(x=10, y=90, width=140, height=30)

        self.label_total_ventas_dia = tk.Entry(label_reportes, font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        self.label_total_ventas_dia.place(x=155, y=90, width=210, height=30)

        # Botón para calcular las ventas del día
        btn_calcular_ventas = tk.Button(label_reportes, text="Calcular Ventas", font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296", command=self.calcular_ventas_dia)
        btn_calcular_ventas.place(x=10, y=150, width=150, height=30)

        # Diferencia de cierres entre ventas y caja
        label_diferencia = tk.Label(label_reportes, text="Diferencia:", font=("sans 12 bold"), bg="#477296", fg="white")
        label_diferencia.place(x=10, y=200, width=140, height=30)
        self.label_diferencia = tk.Entry(label_reportes, font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296")
        self.label_diferencia.place(x=155, y=200, width=210, height=30)
        
        # Botón para calcular la diferencia
        btn_calcular_diferencia = tk.Button(label_reportes, text="Calcular Diferencia", font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296", command=self.diferencia_arqueo)
        btn_calcular_diferencia.place(x=10, y=250, width=150, height=30)

        # Botón para guardar el arqueo
        btn_guardar_arqueo = tk.Button(label_reportes, text="Guardar Arqueo", font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296", command=self.guardar_arqueo)
        btn_guardar_arqueo.place(x=10, y=300, width=150, height=30)

        # Botón para imprimir el arqueo
        boton_imprimir_arqueo_pdf = tk.Button(label_reportes, text="Imprimir Arqueo", font=("sans 12 bold"), bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296", command=self.imprimir_arqueo)
        boton_imprimir_arqueo_pdf.place(x=10, y=350, width=150, height=30)
        

    def diferencia_arqueo(self): # Método para calcular la diferencia entre el total de caja y las ventas del día
        try:
            # Obtener el dinero total en caja
            total_caja = float(self.label_total_caja.get().replace("₵", "").replace(",", "").strip() or 0)
            # Obtener el total de ventas del día
            total_ventas = float(self.label_total_ventas_dia.get().replace("₵", "").replace(",", "").strip() or 0)
            # Calcular la diferencia
            diferencia = total_caja - total_ventas
            # Formatear el resultado y mostrarlo en el Entry
            resultado_formateado = f"₵ {diferencia:,.0f}"
            self.label_diferencia.config(state="normal") # Cambiar el estado a normal para permitir la edición
            self.label_diferencia.delete(0, tk.END)  # Limpiar el campo de entrada
            self.label_diferencia.insert(0, resultado_formateado) # Insertar el resultado formateado
            self.label_diferencia.config(state="readonly") # Cambiar el estado a readonly para evitar la edición
        except ValueError:
            # Si ocurre un error, limpiar el campo
            self.label_diferencia.config(state="normal")
            self.label_diferencia.delete(0, tk.END) # Limpiar el campo de entrada
            self.label_diferencia.config(state="readonly") # Cambiar el estado a readonly para evitar la edición
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo calcular la diferencia: {e}") # Mostrar mensaje de error
            self.label_diferencia.config(state="normal") # Cambiar el estado a normal para permitir la edición
            self.label_diferencia.delete(0, tk.END) # Limpiar el campo de entrada

    def guardar_arqueo(self): # Método para guardar el arqueo en la base de datos
        try:
            # Conexión a la base de datos
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Obtener los valores de las etiquetas
            fecha = datetime.now().strftime('%d-%m-%Y')
            moneda_5 = int(self.label_moneda_5.get() or 0)    # Cantidad de monedas de ₵5
            moneda_10 = int(self.label_moneda_10.get() or 0)    # Cantidad de monedas de ₵10
            moneda_25 = int(self.label_moneda_25.get() or 0)    # Cantidad de monedas de ₵25
            moneda_50 = int(self.label_moneda_50.get() or 0)
            moneda_100 = int(self.label_moneda_100.get() or 0)
            moneda_500 = int(self.label_moneda_500.get() or 0)
            billete_1000 = int(self.label_billete_1000.get() or 0)   # Cantidad de billetes de ₵1.000
            billete_2000 = int(self.label_billete_2000.get() or 0)
            billete_5000 = int(self.label_billete_5000.get() or 0) 
            billete_10000 = int(self.label_billete_10000.get() or 0)
            billete_20000 = int(self.label_billete_20000.get() or 0)
            total_caja = float(self.label_total_caja.get().replace("₵", "").replace(",", "").strip() or 0)
            venta_dia = float(self.label_total_ventas_dia.get().replace("₵", "").replace(",", "").strip() or 0)
            diferencia = float(self.label_diferencia.get().replace("₵", "").replace(",", "").strip() or 0)

            # Insertar los datos en la tabla 'caja'
            cursor.execute('''
                INSERT INTO caja (
                    fecha, moneda_5, moneda_10, moneda_25, moneda_50, moneda_100, moneda_500,
                    billete_1000, billete_2000, billete_5000, billete_10000, billete_20000,
                    total_caja, venta_dia, diferencia
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
            ''', (fecha, moneda_5, moneda_10, moneda_25, moneda_50, moneda_100, moneda_500,
                  billete_1000, billete_2000, billete_5000, billete_10000, billete_20000,
                  total_caja, venta_dia, diferencia))  # Guardar el arqueo en la base de datos

            # Confirmar los cambios y cerrar la conexión
            conn.commit()
            conn.close()

            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", "El arqueo se ha guardado correctamente.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo guardar el arqueo: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error inesperado: {e}")

    def imprimir_arqueo(self):
        try:
            # Ruta del archivo PDF
            fecha_actual = datetime.now().strftime('%d-%m-%Y')
            arqueo_path = os.path.join(self.cierres_caja_folder, f"Cierre_de_Caja_{fecha_actual}.pdf")
            c = canvas.Canvas(arqueo_path, pagesize=letter) # Crear un objeto Canvas para el PDF

            # Información de la empresa
            empresa_nombre = "Carniceria El Asadito S.A"
            empresa_direccion = "San José, avenida 10, calle 3"
            empresa_telefono = "+506 2539-1088"
            empresa_email = "ventas@elasadito.com"
            empresa_website = "www.elasadito.com"

            # Encabezado del PDF
            c.setFont("Helvetica", 18)
            c.setFillColor(colors.darkblue)
            c.drawCentredString(300, 750, f"Cierre de Caja - {fecha_actual}")

            # Información de la empresa
            c.setFillColor(colors.black)
            c.setFont("Helvetica", 12)
            c.drawString(50, 710, f"{empresa_nombre}")
            c.drawString(50, 690, f"Dirección: {empresa_direccion}")
            c.drawString(50, 670, f"Teléfono: {empresa_telefono}")
            c.drawString(50, 650, f"Email: {empresa_email}")
            c.drawString(50, 630, f"Website: {empresa_website}")

            # Línea divisoria
            c.setLineWidth(0.5)
            c.setStrokeColor(colors.gray)
            c.line(50, 620, 550, 620)

             # Información del arqueo
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, 600, f"Fecha: {fecha_actual}") # Ajustar la posición vertical
           
            # Detalle de monedas y billetes 
            y_offset = 500  # Ajustar la posición vertical
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y_offset, "Cantidad de Monedas y Billetes en caja:") # Ajustar la posición vertical
            y_offset -= 20  # Espacio para el título

            detalles = [
                ("Monedas de ¢ 5", self.label_moneda_5.get(), 5),
                ("Monedas de ¢ 10", self.label_moneda_10.get(), 10),
                ("Monedas de ¢ 25", self.label_moneda_25.get(), 25),
                ("Monedas de ¢ 50", self.label_moneda_50.get(), 50),
                ("Monedas de ¢ 100", self.label_moneda_100.get(), 100),
                ("Monedas de ¢ 500", self.label_moneda_500.get(), 500),
                ("Billetes de ¢ 1.000", self.label_billete_1000.get(), 1000),
                ("Billetes de ¢ 2.000", self.label_billete_2000.get(), 2000),
                ("Billetes de ¢ 5.000", self.label_billete_5000.get(), 5000),
                ("Billetes de ¢ 10.000", self.label_billete_10000.get(), 10000),
                ("Billetes de ¢ 20.000", self.label_billete_20000.get(), 20000),
            ]

            for descripcion, cantidad, valor in detalles:
                cantidad = int(cantidad or 0)
                total = cantidad * valor
                c.setFont("Helvetica", 12)
                c.drawString(50, y_offset, f"{descripcion}: {cantidad} unidades")
                c.drawString(300, y_offset, f"Total: ¢ {total:,.0f}")
                y_offset -= 20

            # Dibujar un recuadro para la información adicional
            recuadro_x = 50
            recuadro_y = y_offset - 100  # Ajustar la posición del recuadro
            recuadro_width = 500
            recuadro_height = 100

            c.setStrokeColor(colors.black) # Ajustar el color del borde
            c.setLineWidth(1) # Ajustar el grosor del borde
            c.rect(recuadro_x, recuadro_y, recuadro_width, recuadro_height, stroke=1, fill=0) # Dibujar el recuadro

            # Agregar el texto dentro del recuadro
            c.setFont("Helvetica-Bold", 12)
            c.drawString(recuadro_x + 10, recuadro_y + recuadro_height - 20, f"Saldo Inicial: ¢ {float(self.saldo_inicial.get() or 0):,.0f}")
            c.drawString(recuadro_x + 10, recuadro_y + recuadro_height - 40, f"Total en Caja: ¢ {float(self.label_total_caja.get().replace('₵', '').replace(',', '').strip() or 0):,.0f}")
            c.drawString(recuadro_x + 10, recuadro_y + recuadro_height - 60, f"Ventas del Día: ¢ {float(self.label_total_ventas_dia.get().replace('₵', '').replace(',', '').strip() or 0):,.0f}")
            c.drawString(recuadro_x + 10, recuadro_y + recuadro_height - 80, f"Diferencia: ¢ {float(self.label_diferencia.get().replace('₵', '').replace(',', '').strip() or 0):,.0f}")

            # Guardar el PDF
            c.save()

            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", f"El reporte de arqueo se ha generado correctamente en:\n{arqueo_path}")

            # Abrir el archivo PDF
            os.startfile(os.path.abspath(arqueo_path))

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte de arqueo: {e}")
















