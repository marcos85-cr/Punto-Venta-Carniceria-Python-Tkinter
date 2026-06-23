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
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import datetime
import threading  # Para poder filtrar en el modulo Ventas por nommbre conforme se escribe
from reportlab.lib.pagesizes import letter  # importar el tamaño carta para reportes
from reportlab.lib import colors # importar los colores para el reporte
from reportlab.lib.units import inch # importar las unidades de pulgadas para el reporte
from reportlab.pdfgen import canvas # importa la capacidad de crear PDF
from reportlab.pdfbase.ttfonts import TTFont # importar la capacidad de crear PDF
from reportlab.pdfbase import pdfmetrics # importar la capacidad de crear PDF
from clientes import Clientes # Para importar el listado de clientes del modulo clientes
import sys
import os

"""
    Este módulo define la clase Punto_Venta, que representa la interfaz gráfica y la lógica de negocio para el punto de venta de una carnicería.
    Permite gestionar la venta de productos, calcular totales, aplicar IVA, y generar facturas en formato PDF.
    También incluye funcionalidades para filtrar productos y clientes, así como para actualizar el stock de los productos vendidos.
    Además, permite ver las ventas realizadas y gestionar la base de datos de clientes.
"""


class Punto_Venta(tk.Frame): # Clase que representa el módulo de ventas en el sistema de punto de venta
    db_name = os.path.join(os.path.dirname(__file__), "database.db")  # Ruta dinámica para la base de datos

    def __init__(self, padre):
        super().__init__(padre)
        self.padre = padre
        self.numero_factura = self.obtener_numero_factura_actual() # Obtiene el número de factura actual
        self.productos_seleccionados = [] # Lista para almacenar los productos seleccionados
        self.widgets() # Inicializa los widgets de la interfaz gráfica
        self.cargar_productos() # Carga los productos al iniciar el módulo
        self.cargar_clientes() # Carga los clientes al iniciar el módulo
        self.timer_producto = None # Temporizador para filtrar productos
        self.timer_cliente = None # Temporizador para filtrar clientes

        # Inicia el temporizador para actualizar clientes periódicamente
        self.actualizar_clientes_periodicamente()

    def abrir_gestion_clientes(self): ## Abre la ventana de gestión de clientes
        
        ventana_clientes = Clientes(self.root, update_callback=self.cargar_clientes) # Se pasa la función de actualización como callback
        ventana_clientes.grab_set() # Bloquea la ventana principal hasta que se cierre la ventana de clientes

    def obtener_numero_factura_actual(self): # Función para obtener el número de factura actual
        """Obtiene el número de factura actual de la base de datos."""
        try:
            conn = sqlite3.connect(self.db_name) # Conexión a la base de datos
            c = conn.cursor() # Cursor para ejecutar consultas
            c.execute("SELECT MAX(factura) FROM ventas") # Consulta para obtener el número máximo de factura
            # Si no hay facturas, el resultado será None
            last_invoice_number = c.fetchone()[0]
            conn.close()

            # Determinar el próximo número de factura
            next_invoice_number = last_invoice_number + 1 if last_invoice_number is not None else 1 # Si no hay facturas, empieza desde 1

            return str(next_invoice_number).zfill(4) # Se convierte a string y se rellenan con ceros a la izquierda hasta 4 dígitos

        except sqlite3.Error as e: # Manejo de errores en la conexión a la base de datos
            print("Error obteniendo el número de factura actual: ", e) # Imprime el error en la consola
            return "0001" # Si hay un error, se devuelve 0001 como número de factura inicial
    
    def cargar_clientes(self): #Funcion para cargar los clientes en el cuadro de clientes.
        try:
            conn = sqlite3.connect(self.db_name) # Conexión a la base de datos
            c = conn.cursor()
            c.execute("SELECT nombre FROM clientes") # consulta a la base de datos por medio de filtro
            clientes = c.fetchall() # acá la se almacena la información que se filtro anteriormente
            self.clientes = [cliente[0] for cliente in clientes] # Se extraen los nombres de los clientes
            self.entry_cliente["values"] = self.clientes # Se asignan los valores a la entrada de cliente
            conn.close()
        except sqlite3.Error as e:
            print("Error cargando clientes", e) # Manejo de errores en la conexión a la base de datos

    def actualizar_clientes_periodicamente(self):  
        """Actualiza la lista de clientes cada 3 segundos."""
        self.cargar_clientes() # Llama a la función para cargar clientes
        self.after(3000, self.actualizar_clientes_periodicamente)  # Llama a la función cada 3 segundos

    def filtrar_clientes(self, event): # Filtra los clientes en el cuadro de texto de clientes
        """Filtra los clientes según lo que se escribe en el cuadro de texto."""
        if self.timer_cliente: # Si ya hay un temporizador en ejecución, lo cancela
            self.timer_cliente.cancel() # Cancela el temporizador anterior para evitar múltiples llamadas a la función de filtrado
        # Crea un nuevo temporizador que se ejecuta después de 0.5 segundos
        self.timer_cliente = threading.Timer(0.5, self._filter_clientes) # Temporizador para evitar que se llame a la función demasiado rápido 
        self.timer_cliente.start() # Inicia el temporizador

    def _filter_clientes(self): # Función que se ejecuta después de que el temporizador se apaga
        typed = self.entry_cliente.get() # Obtiene el texto escrito en el cuadro de texto de clientes

        if typed =='': # Si no hay texto, muestra todos los clientes
            data = self.clientes # Se asigna la lista completa de clientes
        else:
            data = [item for item in self.clientes if typed.lower() in item.lower()] # Filtra la lista de clientes según lo que se ha escrito
        
        if data: # Si hay resultados, los muestra en el cuadro de texto
            self.entry_cliente['values'] = data # Se asigna la lista filtrada a la entrada de cliente
            self.entry_cliente.event_generate('<Down>') # Genera un evento de tecla hacia abajo para mostrar la lista desplegable
        else:
            self.entry_cliente['values'] = ['No se encontraron resultados'] # Si no hay resultados, muestra un mensaje de error
            self.entry_cliente.event_generate('<Down>') # Genera un evento de tecla hacia abajo para mostrar la lista desplegable
            self.entry_cliente.delete(0, tk.END) # Borra el texto en el cuadro de texto de clientes

    # carga los productos del inventario en ventas
    def cargar_productos(self): # Carga los productos desde la base de datos
        try:
            conn = sqlite3.connect(self.db_name) # Conexión a la base de datos
            c = conn.cursor()
            c.execute("SELECT articulos FROM articulos") # Consulta para obtener los nombres de los productos
            # Se almacenan los resultados en una lista de tuplas
            self.products = [product[0] for product in c.fetchall()] # Se extraen los nombres de los productos
            # Se asignan los valores a la entrada de producto
            self.entry_producto["values"] = self.products # Se asigna la lista completa de productos a la entrada de producto
            # Se asigna el valor de stock a la etiqueta de stock
            conn.close()
        except sqlite3.Error as e:
            print("Error cargando productos", e) # Manejo de errores en la conexión a la base de datos
    
    # Funcion para filtrar los articulos en el Punto de Ventas
    def filtrar_productos(self, event): # Filtra los productos en el cuadro de texto de productos
        """Filtra los productos según lo que se escribe en el cuadro de texto."""
        if self.timer_producto:
            self.timer_producto.cancel() # Cancela el temporizador anterior para evitar múltiples llamadas a la función de filtrado
        self.timer_producto = threading.Timer(0.5, self._filter_products) # Crea un nuevo temporizador que se ejecuta después de 0.5 segundos
        self.timer_producto.start()

    def _filter_products(self): # Función que se ejecuta después de que el temporizador se apaga
        typed = self.entry_producto.get() # Obtiene el texto escrito en el cuadro de texto de productos
        # Filtra la lista de productos según lo que se ha escrito

        if typed =='': # Si no hay texto, muestra todos los productos
            data = self.products # Se asigna la lista completa de productos
        else:
            data = [item for item in self.products if typed.lower() in item.lower()] # Filtra la lista de productos según lo que se ha escrito
        # Si hay resultados, los muestra en el cuadro de texto
        
        if data:
            self.entry_producto['values'] = data # Se asigna la lista filtrada a la entrada de producto
            self.entry_producto.event_generate('<Down>') # Genera un evento de tecla hacia abajo para mostrar la lista desplegable
        else:
            self.entry_producto['values'] = ['No se encontraron resultados'] # Si no hay resultados, muestra un mensaje de error
            self.entry_producto.event_generate('<Down>') 
            self.entry_producto.delete(0, tk.END) # Borra el texto en el cuadro de texto de productos

    def agregar_articulo(self): # Agrega un artículo a la venta
        cliente = self.entry_cliente.get() # Obtiene el cliente seleccionado
        # Si no hay cliente seleccionado, muestra un mensaje de error
        producto = self.entry_producto.get() # Obtiene el producto seleccionado
        # Si no hay producto seleccionado, muestra un mensaje de error
        cantidad = self.entry_cantidad.get() # Obtiene la cantidad ingresada

        # Validación que no pueden haber espacios en blanco en ventas
        if not cliente: # Validación de cliente
            messagebox.showerror("Error", "Por favor seleccione un cliente") # Muestra un mensaje de error si no hay cliente seleccionado
            return

        if not producto:
            messagebox.showerror("Error", "Por favor seleccione un producto") # Muestra un mensaje de error si no hay producto seleccionado
            return

        try:
            cantidad = float(cantidad) # Convierte la cantidad a un número flotante
            if cantidad <= 0: # Validación de cantidad
                raise ValueError # Si la cantidad es menor o igual a 0, lanza un error
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese una cantidad válida")
            return

        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT precio, costo, stock FROM articulos WHERE articulos=?", (producto,)) # Consulta para obtener el precio, costo y stock del producto seleccionado
            resultado = c.fetchone()

            if resultado is None: # Validación de producto
                messagebox.showerror("Error", "Producto no encontrado")
                return

            precio, costo, stock = resultado # Desempaqueta el resultado de la consulta
            

            if cantidad > stock: # Validación de stock
                messagebox.showerror("Error", f"Stock insuficiente, únicamente hay {stock} unidades disponibles.") # Muestra un mensaje de error si la cantidad solicitada es mayor que el stock disponible
                return
            # cálculo del iva
            total = precio * cantidad
            iva = total * 0.13  # Calcula el 13% del total como IVA
            total_con_iva = total + iva

            # Formatear para mostrar en la interfaz
            total_colon = "{:,.0f}".format(total_con_iva) # Formatea el total con separadores de miles y sin decimales
            iva_colon = "{:,.0f}".format(iva) # Formatea el IVA con separadores de miles y sin decimales

            # Insertar en el Treeview
            self.tre.insert("", "end", values=(self.numero_factura, cliente, cantidad,
                                               producto, "{:,.0f}".format(precio), iva_colon, total_colon)) # Inserta el artículo en el Treeview con los valores formateados
            # Guardar en la lista de productos seleccionados
            self.productos_seleccionados.append((self.numero_factura, cliente, producto, precio, cantidad, total, iva, costo)) # Agrega el artículo a la lista de productos seleccionados
            # Actualizar el stock en la base de datos

            conn.close() # Cierra la conexión a la base de datos

            # Limpiar campos
            self.entry_producto.set('') # Limpia el campo de producto
            self.entry_cantidad.delete(0, 'end')

        except sqlite3.Error as e:
            print("Error al agregar el artículo", e) # Manejo de errores en la conexión a la base de datos

        self.calcular_precio_total() # Calcular el total después de agregar el artículo

    def calcular_precio_total(self): # Calcular el total de la venta
        total_pagar = sum(float(str(self.tre.item(item)["values"][-1]).replace(" ", "").replace(",", "")) for item in self.tre.get_children())
        total_pagar_colon = "{:,.0f}".format(total_pagar) # Formatea el total con separadores de miles y sin decimales
        self.label_precio_total.config(text=f"Precio a pagar: ₵ {total_pagar_colon}") # Actualiza la etiqueta del precio total

    def actualizar_stock(self, event=None): # Actualiza el stock del producto seleccionado
        producto_seleccionado = self.entry_producto.get()

        try: 
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT stock FROM articulos WHERE articulos=?", (producto_seleccionado,)) # Consulta para obtener el stock del producto seleccionado
            stock = c.fetchone() # Se obtiene el stock del producto seleccionado
            conn.close() # Cierra la conexión a la base de datos

            self.label_stock.config(text=f"Stock: {stock[0]}") # Actualiza la etiqueta del stock con el valor obtenido
        except sqlite3.Error as e:
            print("Error al obtener el stock del producto",e)



    def realizar_pago(self): # Realiza el pago de la venta
        if not self.tre.get_children(): # Verifica si hay productos en el Treeview
            messagebox.showerror("Error", "No hay productos seleccionados para realizar el pago.")
            return

        # Calcular el total directamente desde el Treeview para garantizar consistencia
        total_venta = sum(float(str(self.tre.item(item)["values"][-1]).replace(",", "").replace("₵", "").strip()) 
            for item in self.tre.get_children() 
        ) # Sumar el total de cada artículo en el Treeview
        # Formatear el total para mostrarlo en la ventana de pago

        total_formateado = "{:,.0f}".format(total_venta) # Formatear el total para mostrarlo en la ventana de pago

        ventana_pago = tk.Toplevel(self)
        ventana_pago.title("Realizar pago")
        ventana_pago.geometry("400x400+450+80") # Tamaño y posición de la ventana de pago
        ventana_pago.config(bg="#477296")
        ventana_pago.resizable(False, False) # Deshabilitar el cambio de tamaño de la ventana
        ventana_pago.transient(self.master) # Mantener la ventana de pago encima de la ventana principal
        ventana_pago.grab_set()     # Bloquear la ventana principal hasta que se cierre la ventana de pago
        ventana_pago.focus_set()    # Focalizar la ventana de pago para que el usuario pueda interactuar con ella
        ventana_pago.lift()         # Llevar la ventana de pago al frente

        def abrir_ventana_efectivo():
            ventana_efectivo = tk.Toplevel(ventana_pago)
            ventana_efectivo.title("Pago en efectivo")
            ventana_efectivo.geometry("400x400+450+80")
            ventana_efectivo.config(bg="#477296")
            ventana_efectivo.resizable(False, False) 
            ventana_efectivo.transient(self.master) 
            ventana_efectivo.grab_set() 


            label_titulo = tk.Label(ventana_efectivo, text="Realizar pago en efectivo", font="sans 20 bold", bg="#477296")
            label_titulo.pack(pady=10)

            tk.Label(ventana_efectivo, text="Ingrese monto en efectivo:", bg="#477296", font="sans 16").pack(pady=40)
            entry_monto = tk.Entry(ventana_efectivo, font="sans 16", bg="white", fg="black")
            entry_monto.pack()
    
            def confirmar_pago_efectivo():  
                try:
                    monto = float(entry_monto.get())
                    if monto < total_venta:
                        messagebox.showerror("Error", "Monto insuficiente.")
                    else:
                        cambio = monto - total_venta
                        messagebox.showinfo("Pago exitoso", f"Pago recibido.\nCambio: ₵ {cambio:,.0f}")
                        ventana_efectivo.destroy()
                        ventana_pago.destroy()
                        self.finalizar_pago(total_venta)
                except ValueError:
                    messagebox.showerror("Error", "Ingrese un número válido.")

            tk.Button(ventana_efectivo, text="Confirmar pago", font="sans 16 bold", borderwidth=0, highlightthickness=0, command=lambda: self.procesar_pago(entry_monto.get(), ventana_pago, total_venta)).pack(pady=20)

           

        def abrir_ventana_tarjeta():
            ventana_tarjeta = tk.Toplevel(ventana_pago)
            ventana_tarjeta.title("Pago con tarjeta")
            ventana_tarjeta.geometry("400x350+470+100")
            ventana_tarjeta.config(bg="#477296")
            ventana_tarjeta.resizable(False, False) 
            ventana_tarjeta.transient(self.master) 
            ventana_tarjeta.grab_set() 

            tk.Label(ventana_tarjeta, text="Pago con tarjeta", font="sans 20 bold", bg="#477296", fg="white").pack(pady=10)

            tk.Label(ventana_tarjeta, text="Número de tarjeta:", bg="#477296", font="sans 16").pack(pady=5)
            entry_numero = tk.Entry(ventana_tarjeta, font="sans 16", bg="white", fg="black")
            entry_numero.pack()

            tk.Label(ventana_tarjeta, text="Fecha de vencimiento (MM/AA):", bg="#477296", font="sans 16").pack(pady=5)
            entry_vencimiento = tk.Entry(ventana_tarjeta, font="sans 16", bg="white", fg="black")
            entry_vencimiento.pack()

            tk.Label(ventana_tarjeta, text="CVV:", bg="#477296", font="sans 16").pack(pady=5)
            entry_cvv = tk.Entry(ventana_tarjeta, font="sans 16", show="*", bg="white", fg="black")
            entry_cvv.pack()

            def confirmar_pago_tarjeta():
                numero = entry_numero.get()
                vencimiento = entry_vencimiento.get()
                cvv = entry_cvv.get()

                if len(numero) != 16 or not numero.isdigit():
                    messagebox.showerror("Error", "Número de tarjeta inválido.")
                    return
                if not cvv.isdigit() or len(cvv) != 3:
                    messagebox.showerror("Error", "CVV inválido.")
                    return
                if "/" not in vencimiento or len(vencimiento) != 5:
                    messagebox.showerror("Error", "Fecha de vencimiento inválida. Use el formato MM/AA.")
                    return

                messagebox.showinfo("Pago exitoso", "Pago con tarjeta procesado correctamente.")
                ventana_tarjeta.destroy()
                self.finalizar_pago(total_venta)  # Asegúrate que `total_venta` esté disponible en este contexto

            tk.Button(ventana_tarjeta,text="Confirmar pago",font="sans 16 bold",borderwidth=0, highlightthickness=0,command=lambda: self.procesar_pago(total_venta, ventana_pago, total_venta)).pack(pady=20)

         
        # Creación de etiquetas y campos de entrada en la ventana de pago
        label_titulo = tk.Label(ventana_pago, text="Realizar pago", font="sans 24 bold", bg="#477296") # Etiqueta para el título
        label_titulo.place(x=120, y=10)

        label_total = tk.Label(ventana_pago, text=f"Total a pagar: ₵ {total_formateado}", font="sans 18 bold", bg="#477296") # Etiqueta para el total a pagar
        label_total.place(x=100, y=100)


        #botones para pagos

        button_efectivo = tk.Button(ventana_pago, text="Pagar en efectivo", bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296",
                                    font="sans 16 bold", command=abrir_ventana_efectivo)
        button_efectivo.place(x=80, y=180, width=240, height=40)

        button_tarjeta = tk.Button(ventana_pago, text="Pagar con tarjeta",bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296" , 
                                    font="sans 16 bold", command=abrir_ventana_tarjeta)
        button_tarjeta.place(x=80, y=230, width=240, height=40)


    def procesar_pago(self, cantidad_pagada, ventana_pago, total_venta): # Validar el pago
        """Procesa el pago y genera la factura."""

        try:
            cantidad_pagada = float(cantidad_pagada) # Convierte la cantidad pagada a un número flotante
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto válido.") # Si la conversión falla, muestra un mensaje de error
            return

        cliente = self.entry_cliente.get() # Obtiene el cliente seleccionado

        if cantidad_pagada < total_venta: 
            messagebox.showerror("Error", "La cantidad pagada es insuficiente.") # Si la cantidad pagada es menor que el total de la venta, muestra un mensaje de error
            return
        
        cambio = cantidad_pagada - total_venta # Calcula el cambio a devolver al cliente

        total_formateado = "{:,.0f}".format(total_venta) # Formatea el total para mostrarlo en la ventana de pago

        mensaje = f"Total ₵: {total_formateado} \nCantidad pagada ₵: {cantidad_pagada:,.0f} \nCambio ₵: {cambio:,.0f}" # Aca me indica el vuelto de la compra
        messagebox.showinfo("Pago realizado", mensaje) # Muestra un mensaje de información con el total, la cantidad pagada y el cambio
        # Generar el PDF de la factura
        
        # Registrar el pago en la base de datos
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            fecha_actual = datetime.datetime.now().strftime("%d-%m-%Y") # Formato de fecha
            hora_actual = datetime.datetime.now().strftime("%H:%M:%S") # Formato de hora

            # Actualiza la cantidad de productos en la base de datos
            for item in self.productos_seleccionados:
                factura, cliente, articulos, precio, cantidad, total, IVA, costo = item # Desempaqueta los valores del artículo seleccionado
                c.execute("INSERT INTO ventas (factura, cliente, articulos, cantidad, precio, IVA, total, costo, fecha, hora) VALUES (?,?,?,?,?,?,?,?,?,?)",
                          (factura, cliente, articulos, cantidad, precio, IVA, total, costo * cantidad, fecha_actual, hora_actual)) # Inserta la venta en la base de datos
                # Actualiza el stock del producto vendido

                c.execute("UPDATE articulos SET stock = stock - ? WHERE articulos = ?", (cantidad, articulos)) 
            
            conn.commit()

            self.generar_factura_pdf(total_venta, cliente) # Genera el PDF de la factura


        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al registrar la venta: {e}") # Manejo de errores en la conexión a la base de datos

        self.numero_factura = str(int(self.numero_factura) + 1) # Incrementa el número de factura para la próxima venta
        self.label_numero_factura.config(text=self.numero_factura) # Actualiza la etiqueta del número de factura

        self.productos_seleccionados = [] # Limpia la lista de productos seleccionados
        self.limpiar_campos() # Limpia los campos de entrada y el Treeview

        ventana_pago.destroy() # Cierra la ventana de pago


    def limpiar_campos(self): # Limpia los campos de entrada y el Treeview
        for item in self.tre.get_children():
            self.tre.delete(item)
        self.label_precio_total.config(text="Precio a pagar: ₵ 0") # Resetea el precio total a 0

        self.entry_producto.set('') # Limpia el campo de producto
        self.entry_cantidad.delete(0, 'end') # Limpia el campo de cantidad

    def limpiar_lista(self): # Limpia la lista de productos seleccionados
        self.tre.delete(*self.tre.get_children()) # Elimina todos los elementos del Treeview
        self.productos_seleccionados.clear() # Limpia la lista de productos seleccionados
        self.calcular_precio_total() # Recalcula el precio total a 0
    
    def eliminar_articulo(self): # Elimina el artículo seleccionado del Treeview y de la lista de productos seleccionados
        item_seleccionado = self.tre.selection() # Obtiene el artículo seleccionado en el Treeview
        if not item_seleccionado:
            messagebox.showerror("Error", "No hay ningun artículo seleccionado")
            return

        item_id = item_seleccionado[0] # Obtiene el ID del artículo seleccionado
        valores_item = self.tre.item(item_id)["values"] # Obtiene los valores del artículo seleccionado
        factura, cliente, articulo, precio, cantidad, total = valores_item # Desempaqueta los valores del artículo seleccionado

        self.tre.delete(item_id) # Elimina el artículo del Treeview

        # Filtra la lista de productos seleccionados para eliminar el artículo seleccionado
        self.productos_seleccionados = [producto for producto in self.productos_seleccionados if producto[2] != articulo] 

        self.calcular_precio_total() # Recalcula el precio total después de eliminar el artículo
        # Actualiza el stock del producto en la base de datos
    
    def editar_articulo(self): # Funcion para editar el articulo seleccionado
        selected_item = self.tre.selection() # Obtiene el artículo seleccionado en el Treeview
        if not selected_item: # Verifica si hay un artículo seleccionado
            messagebox.showerror("Error", "Por favor seleccione un artículo para editar")
            return

        item_values = self.tre.item(selected_item[0], 'values') # Obtiene los valores del artículo seleccionado
        if not item_values: # Verifica si hay valores en el artículo seleccionado
            return

        try:
            current_cantidad = float(item_values[2]) # Obtiene la cantidad actual del artículo seleccionado
        except ValueError:
            messagebox.showerror("Error", "El valor de la cantidad no es válido.")
            return

        # Muestra un cuadro de diálogo para ingresar la nueva cantidad
        new_cantidad = simpledialog.askfloat("Editar artículo", "Ingrese la nueva cantidad:", initialvalue=current_cantidad) 

        if new_cantidad is not None:
            try:
                conn = sqlite3.connect(self.db_name) # Conexión a la base de datos
                # Verifica si la nueva cantidad es válida
                c = conn.cursor()
                # Consulta para obtener el precio, costo y stock del producto seleccionado
                c.execute("SELECT precio, costo, stock FROM articulos WHERE articulos=?", (item_values[3],)) 
                resultado = c.fetchone() # Se obtiene el resultado de la consulta

                if resultado is None: # Verifica si el producto existe en la base de datos
                    messagebox.showerror("Error", "Producto no encontrado en la base de datos")
                    conn.close()
                    return

                precio, costo, stock = resultado # Desempaqueta el resultado de la consulta

                if new_cantidad > stock: # Verifica si la nueva cantidad es mayor que el stock disponible
                    messagebox.showerror("Error", f"Stock insuficiente. Solamente quedan {stock} unidades disponibles")
                    conn.close()
                    return

                # Recalcular el total y el IVA
                total = precio * new_cantidad 
                iva = total * 0.13  # 13% de IVA
                total_con_iva = total + iva # Muestra el valor total incluyendo el IVA

                # Actualizar el Treeview
                self.tre.item(selected_item[0], values=(self.numero_factura, self.entry_cliente.get(), new_cantidad,
                                                        item_values[3], "{:,.0f}".format(precio), "{:,.0f}".format(iva),
                                                        "{:,.0f}".format(total_con_iva)))

                # Actualizar la lista de productos seleccionados
                for idx, producto in enumerate(self.productos_seleccionados):
                    if producto[2] == item_values[3]:  # Verifica que el producto coincida
                        # Actualiza la cantidad y el total en la lista de productos seleccionados
                        self.productos_seleccionados[idx] = (self.numero_factura, self.entry_cliente.get(), item_values[3],
                                                             precio, new_cantidad, total, iva, costo)
                        break

                conn.close() # Cierra la conexión a la base de datos

                # Recalcular el precio total después de la actualización
                self.calcular_precio_total() # Llama a la función para recalcular el precio total
            except sqlite3.Error as e:
                print("Error al editar el artículo: ", e)

    def ver_ventas_realizadas(self): # Funcion para ver las ventas realizadas
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT * FROM ventas")
            ventas = c.fetchall() # captura los registros de ventas
            conn.close()

            ventana_ventas = tk.Toplevel(self)
            ventana_ventas.title("Ventas Realizadas")
            ventana_ventas.geometry("1100x650+120+20")
            ventana_ventas.config(bg="#477296")
            ventana_ventas.resizable(False,False) # para que no se pueda cambiar el tamaño con el cursor
            ventana_ventas.transient(self.master) # Para que no se pueda manipular las demas ventanas mientras este este en uso
            ventana_ventas.grab_set() # Para que no se pueda manipular las demas ventanas mientras este este en uso
            ventana_ventas.focus_set() # Para que la ventana de ventas tenga el foco
            ventana_ventas.lift() # Para que la ventana de ventas se muestre por encima de las demas ventanas   

            def filtrar_ventas():  # Funcion para filtrar las ventas realizadas
                """Filtra las ventas realizadas según el número de factura y el cliente."""
                factura_a_buscar = entry_factura.get()
                cliente_a_buscar = entry_cliente.get()
                for item in tree.get_children(): # Elimina todos los elementos del Treeview
                    tree.delete(item)

                ventas_filtradas = [
                    venta for venta in ventas
                    if (str(venta[0])==factura_a_buscar or not factura_a_buscar) and
                    (venta[1].lower() == cliente_a_buscar.lower() or not cliente_a_buscar)
                ]                                                                # Filtra las ventas según el número de factura y el cliente
                for venta in ventas_filtradas:
                    venta = list(venta) # Convierte la tupla a lista para poder modificarla
                    venta[3] = "{:,.0f}".format(venta[3])  # Formatea el precio
                    venta[4] = "{:,.0f}".format(venta[4])
                    venta[8] = datetime.datetime.strptime(venta[8], "%d-%m-%Y").strftime("%d-%m-%Y") # Formatea la fecha
                    tree.insert("", "end", values=venta) # Inserta la venta filtrada en el Treeview

            # Se crea la ventana de ventas realizadas
            label_ventas_realizadas = tk.Label(ventana_ventas, text="Ventas Realizadas", font="sans 26 bold", bg="#477296")
            label_ventas_realizadas.place(x=350, y=20)

            filtro_frame = tk.Frame(ventana_ventas, bg="#477296") # Se crea el frame para los filtros
            filtro_frame.place(x=20, y=60, width=1060, height=60) # Se coloca el frame en la ventana de ventas realizadas

            label_factura = tk.Label(filtro_frame, text="Número de factura", bg="#477296", font="sans 14 bold") # Etiqueta para el número de factura
            label_factura.place(x=10, y=15)

            entry_factura = ttk.Entry(filtro_frame, font="sans 14 bold") # Campo de entrada para el número de factura
            entry_factura.place(x=200, y=10, width=200, height=40)

            label_cliente = tk.Label(filtro_frame, text="Cliente", bg="#477296", font="sans 14 bold") # Etiqueta para el cliente
            label_cliente.place(x=420, y=15)

            entry_cliente = ttk.Entry(filtro_frame, font="sans 14 bold") # Campo de entrada para el cliente
            entry_cliente.place(x=500, y=10, width=250, height=40)
            # Se asigna la función de filtrado al evento de escritura en el campo de cliente
            btn_filtrar = tk.Button(filtro_frame, text="Filtrar", font="sans 14 bold", bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296", command=filtrar_ventas)
            btn_filtrar.place(x=770, y=10)

            tree_frame = tk.Frame(ventana_ventas, bg="white") # Se crea el frame para el Treeview
            tree_frame.place(x=20, y=130, width=1060, height=500)

            scrol_y = ttk.Scrollbar(tree_frame) # Se crea la barra de desplazamiento vertical
            scrol_y.pack(side=RIGHT, fill=Y)

            scrol_x = ttk.Scrollbar(tree_frame, orient=HORIZONTAL) # Se crea la barra de desplazamiento horizontal
            scrol_x.pack(side=BOTTOM, fill=X)

            # Encabezados de las columnas
            tree = ttk.Treeview(tree_frame, columns=("Factura", "Cliente", "Producto", 
                                                    "Precio", "Cantidad", "Total", "IVA","Costo", "Fecha", "Hora"), show="headings")
            tree.pack(expand=TRUE, fill=BOTH) # Se coloca el Treeview en el frame

            scrol_y.config(command=tree.yview) # Se asigna la barra de desplazamiento vertical al Treeview
            scrol_x.config(command=tree.xview) # Se asigna la barra de desplazamiento horizontal al Treeview

            tree.heading("Factura", text="Factura") # Encabezado de la columna de cada uno de las opciones
            tree.heading("Cliente", text="Cliente")
            tree.heading("Producto", text="Producto")
            tree.heading("Precio", text="Precio")
            tree.heading("Cantidad", text="Cantidad")
            tree.heading("Total", text="Total")
            tree.heading("IVA", text="IVA")
            tree.heading("Costo", text="Costo")
            tree.heading("Fecha", text="Fecha")
            tree.heading("Hora", text="Hora")

            # Caracteristicas de las columnas
            tree.column("Factura", width=60, anchor="center") # Ancho y alineación de las columnas
            tree.column("Cliente", width=120, anchor="center")
            tree.column("Producto", width=120, anchor="center")
            tree.column("Precio", width=80, anchor="center")
            tree.column("Cantidad", width=80, anchor="center")
            tree.column("Total", width=80, anchor="center")
            tree.column("IVA", width=50, anchor="center")
            tree.column("Costo", width=50, anchor="center")
            tree.column("Fecha", width=80, anchor="center")
            tree.column("Hora", width=80, anchor="center")

            for venta in ventas: # Se itera sobre las ventas obtenidas de la base de datos
                venta = list(venta)
                venta[3] = "{:,.0f}".format(venta[3]) # Formatea el precio
                venta[5] = "{:,.0f}".format(venta[5])
                venta[8] = datetime.datetime.strptime(venta[8], "%d-%m-%Y").strftime("%d-%m-%Y")
                tree.insert("", "end", values=venta)

        except sqlite3.Error as e:
            messagebox.showerror("Error","Error al obtener las ventas: ", e)

    # Se va crear la factura PDF
    def generar_factura_pdf(self, total_venta, cliente): # Genera la factura en formato PDF
        try:
            # Crear la carpeta "facturas" si no existe
            if not os.path.exists("facturas"): 
                os.makedirs("facturas") 

            factura_path = f"facturas/Factura_{self.numero_factura}.pdf"  # Ruta del archivo PDF
            c = canvas.Canvas(factura_path, pagesize=letter)  # Crear el lienzo del PDF

            # Información de la empresa
            empresa_nombre = "Carniceria El Asadito S.A" 
            empresa_direccion = "San José, avenida 10, calle 3"
            empresa_telefono = "+506 2539-1088"
            empresa_email = "ventas@elasadito.com"
            empresa_website = "www.elasadito.com"

            # Encabezado del PDF
            c.setFont("Helvetica", 18) 
            c.setFillColor(colors.darkblue) #
            c.drawCentredString(300, 750, "FACTURA DE PRODUCTOS")

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

            # Información de la factura
            c.drawString(50, 600, f"Número de Factura: {self.numero_factura}")
            c.drawString(50, 580, f"Fecha: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
            c.drawString(50, 560, f"Cliente: {cliente}")

            # Tabla de productos
            c.drawString(50, 540, "Descripción de Productos:")
            y_offset = 520
            c.setFont("Helvetica", 12)
            c.drawString(70, y_offset, "Producto") # Encabezados de la tabla
            c.drawString(270, y_offset, "Cantidad")
            c.drawString(370, y_offset, "Precio ¢")
            c.drawString(470, y_offset, "Total ¢")
            c.line(50, y_offset - 10, 550, y_offset - 10)  # Línea debajo del encabezado
            y_offset -= 30

            # Agregar productos al PDF
            total_iva = 0  # Variable para acumular el IVA
            for item in self.productos_seleccionados: # Itera sobre los productos seleccionados
                factura, cliente, producto, precio, cantidad, total, iva, costo = item
                c.drawString(70, y_offset, producto)
                c.drawString(270, y_offset, str(cantidad))
                c.drawString(370, y_offset, f"¢{precio:,.0f}")
                c.drawString(470, y_offset, f"¢{total:,.0f}")
                total_iva += iva  # Acumular el IVA
                y_offset -= 20

            # Línea final
            c.line(50, y_offset, 550, y_offset) # Línea debajo de la tabla
            y_offset -= 20

            # Mostrar el IVA total
            c.setFont("Helvetica", 12) # Cambia la fuente para el IVA total
            c.setFillColor(colors.black) 
            c.drawString(50, y_offset, f"IVA Total: ¢ {total_iva:,.0f}")
            y_offset -= 20

            # Total a pagar
            c.setFont("Helvetica", 14)
            c.setFillColor(colors.darkblue) # Cambia el color de la fuente para el total
            c.drawString(50, y_offset, f"Total a Pagar: ¢ {total_venta:,.0f}")
            c.setFillColor(colors.black) 

            # Mensaje de agradecimiento
            y_offset -= 40
            c.setFont("Helvetica", 16)
            c.drawString(150, y_offset, "¡Muchas gracias por su compra!")

            # Términos y condiciones en la factura
            y_offset -= 60
            c.setFont("Helvetica", 10)
            c.drawString(50, y_offset, "Términos y Condiciones:")
            c.drawString(50, y_offset - 20, "1. Para cualquier reclamo, se necesita la factura.")
            c.drawString(50, y_offset - 40, "2. Revise su vuelto antes de salir del local.")
            c.drawString(50, y_offset - 60, "3. Promociones válidas solo en nuestra página web.")

            # Guardar el PDF
            c.save()

            # Mostrar mensaje de éxito
            messagebox.showinfo("Factura Generada", f"Se ha generado la factura en: {factura_path}")

            # Abrir el archivo PDF
            os.startfile(os.path.abspath(factura_path))

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar la factura: {e}") # Manejo de errores al generar la factura PDF

    def widgets(self): # Interfaz grafica
        # Crear rutas dinámicas para las imágenes
        iconos_path = os.path.join(os.path.dirname(__file__), "iconos") # Ruta de la carpeta de iconos
        imagenes = {
            "limpiar": os.path.join(iconos_path, "limpiar.png"),
            "editar": os.path.join(iconos_path, "editar.png"),
            "eliminar": os.path.join(iconos_path, "eliminar.png"),
            "agregar": os.path.join(iconos_path, "agregar.png"),
            "pagar": os.path.join(iconos_path, "pagar.png"),
            "ventas": os.path.join(iconos_path, "informe_ventas.png"),
        } # Diccionario con las rutas de las imágenes

        # Verificar si las imágenes existen antes de cargarlas
        def cargar_imagen(ruta): # Función para cargar las imágenes
            if os.path.exists(ruta):
                imagen_pil = Image.open(ruta)
                imagen_resize = imagen_pil.resize((30, 30))
                return ImageTk.PhotoImage(imagen_resize)
            else:
                print(f"Advertencia: No se encontró la imagen {ruta}") # Mensaje de advertencia si la imagen no se encuentra
                return None

        imagen_tk_limpiar = cargar_imagen(imagenes["limpiar"]) # Carga las imagenes de los botones
        imagen_tk_editar = cargar_imagen(imagenes["editar"])
        imagen_tk_eliminar = cargar_imagen(imagenes["eliminar"])
        imagen_tk_agregar = cargar_imagen(imagenes["agregar"])
        imagen_tk_pagar = cargar_imagen(imagenes["pagar"])
        imagen_tk_ventas = cargar_imagen(imagenes["ventas"])

        # Crear frame y botones para ingresar:Cliente, Producto, Cantidad, Factura N°, Stock
        labelframe = tk.LabelFrame(self,relief="raised", borderwidth=1, font="sans 16 bold", bg="#477296")
        labelframe.place(x=25, y=30, width=1150, height=180)

        label_cliente = tk.Label(labelframe, text="Cliente: ", font="sans 14 bold", bg="#477296") # Etiqueta para el cliente
        label_cliente.place(x=10, y=11)
        self.entry_cliente = ttk.Combobox(labelframe, font="sans 14 bold") # Combobox para seleccionar el cliente
        self.entry_cliente.place(x=120, y=8, width=260, height=40)
        self.entry_cliente.bind('<KeyRelease>', self.filtrar_clientes)
        
        label_producto = tk.Label(labelframe, text="Producto: ", font="sans 14 bold", bg="#477296") # Etiqueta para el producto
        label_producto.place(x=10, y=70)
        self.entry_producto = ttk.Combobox(labelframe, font="sans 14 bold")
        self.entry_producto.place(x=120, y=66, width=260, height=40)
        self.entry_producto.bind('<KeyRelease>', self.filtrar_productos)

        label_cantidad = tk.Label(labelframe, text="Cantidad: ", font="sans 14 bold", bg="#477296") # Etiqueta para la cantidad
        label_cantidad.place(x=500, y=11)
        self.entry_cantidad = ttk.Entry(labelframe, font="sans 14 bold")
        self.entry_cantidad.place(x=610, y=8, width=100, height=40)

        self.label_stock = tk.Label(labelframe, text="Stock: ", font="sans 14 bold", bg="#477296")
        self.label_stock.place(x=500, y=70 )
        self.entry_producto.bind("<<ComboboxSelected>>", self.actualizar_stock) # Actualiza la cantidad de productos en VENTAS


        label_factura = tk.Label(labelframe, text="Factura N°:", font="sans 14 bold",bg="#477296" )
        label_factura.place(x=750, y=11)

        self.label_numero_factura = tk.Label(labelframe, text=f"{self.numero_factura}", font="sans 14 bold", bg="#477296")
        self.label_numero_factura.place(x=950, y=11)

        #Boton Agregar
        boton_agregar = tk.Button(labelframe, text="Agregar", bg="#D3D3D3", highlightthickness=0, relief="flat", borderwidth=0, font="sans 14 bold", command=self.agregar_articulo)
        if imagen_tk_agregar:
            boton_agregar.config(image=imagen_tk_agregar, compound=LEFT, padx=15) # Configura el botón con la imagen
            boton_agregar.image = imagen_tk_agregar
        boton_agregar.place(x=90, y=120, width=200, height=40)

        # Boton Eliminar
        boton_eliminar = tk.Button(labelframe, text="Eliminar", bg="#D3D3D3", highlightthickness=0, relief="flat", borderwidth=0, font="sans 14 bold", command=self.eliminar_articulo)
        if imagen_tk_eliminar:
            boton_eliminar.config(image=imagen_tk_eliminar, compound=LEFT, padx=15) # Configura el botón con la imagen
            boton_eliminar.image = imagen_tk_eliminar
        boton_eliminar.place(x=310, y=120, width=200, height=40)

        # Boton Editar
        boton_editar = tk.Button(labelframe, text="Editar", bg="#D3D3D3", highlightthickness=0, relief="flat", borderwidth=0, font="sans 14 bold", command=self.editar_articulo)
        if imagen_tk_editar:
            boton_editar.config(image=imagen_tk_editar, compound=LEFT, padx=15)
            boton_editar.image = imagen_tk_editar
        boton_editar.place(x=530, y=120, width=200, height=40)

        # Boton Limpiar
        boton_limpiar = tk.Button(labelframe, text="Limpiar", bg="#D3D3D3", highlightthickness=0, relief="flat", borderwidth=0, font="sans 14 bold", command=self.limpiar_lista)
        if imagen_tk_limpiar:
            boton_limpiar.config(image=imagen_tk_limpiar, compound=LEFT, padx=15)
            boton_limpiar.image = imagen_tk_limpiar
        boton_limpiar.place(x=750, y=120, width=200, height=40)

        # Creaar frame para ingresar los artículos a vender
        treFrame = tk.Frame(self,bg="white")
        treFrame.place(x=70, y=220, width=1050, height=300)

        scrol_y = ttk.Scrollbar(treFrame) # Se crea la barra de desplazamiento vertical
        scrol_y.pack(side=RIGHT, fill=Y) # Se crea la barra de desplazamiento vertical

        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL) # Se crea la barra de desplazamiento horizontal
        scrol_x.pack(side=BOTTOM, fill=X)   # Se crea la barra de desplazamiento horizontal

        self.tre = ttk.Treeview(treFrame, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, 
                                height=40, columns=("Factura", "Cliente", "Cantidad", "Producto",
                                                    "Precio", "IVA", "Total"), show="headings") # crea el Treeview
        self.tre.pack(expand=True, fill=BOTH) # Se coloca el Treeview en el frame

        scrol_y.config(command=self.tre.yview) # Se asigna la barra de desplazamiento vertical al Treeview
        scrol_x.config(command=self.tre.xview)  # Se asigna la barra de desplazamiento horizontal al Treeview

        # Establece los nombre de las columnas donde se insertar los productos a vender
        self.tre.heading("Factura", text="Factura")
        self.tre.heading("Cliente", text="Cliente")
        self.tre.heading("Cantidad", text="Cantidad")
        self.tre.heading("Producto", text="Producto")
        self.tre.heading("Precio", text="Precio")
        self.tre.heading("IVA", text="IVA")
        self.tre.heading("Total", text="Total")
        
        self.tre.column("Factura", width=60, anchor="center") # Ancho y alineación de las columnas
        self.tre.column("Cliente", width=250, anchor="center")
        self.tre.column("Cantidad", width=60, anchor="center")
        self.tre.column("Producto", width=250, anchor="center")
        self.tre.column("Precio", width=120, anchor="center")
        self.tre.column("IVA", width=80, anchor="center")
        self.tre.column("Total", width=150, anchor="center")
        self.label_precio_total = tk.Label(self, text="Precio a pagar: ₵ 0.0",  font="sans 18 bold", fg="black", bg="#477296")
        self.label_precio_total.place(x=680, y=550)

        # insertar imaganes en los botones
        boton_pagar = tk.Button(self, text="Pagar", bg="#D3D3D3", highlightthickness=0, relief="flat", borderwidth=0, font="sans 14 bold", command=self.realizar_pago)
        if imagen_tk_pagar:
            boton_pagar.config(image=imagen_tk_pagar, compound=LEFT, padx=15)
            boton_pagar.image = imagen_tk_pagar
        boton_pagar.place(x=70, y=550, width=180, height=40)

        boton_ver_ventas = tk.Button(self, text="Ventas Realizadas", bg="#D3D3D3", highlightthickness=0, relief="flat", borderwidth=0, font="sans 14 bold", command=self.ver_ventas_realizadas)
        if imagen_tk_ventas:
            boton_ver_ventas.config(image=imagen_tk_ventas, compound=LEFT, padx=15)
            boton_ver_ventas.image = imagen_tk_ventas
        boton_ver_ventas.place(x=290, y=550, width=280, height=40)





