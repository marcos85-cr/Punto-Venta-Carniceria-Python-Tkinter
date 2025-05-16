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
from tkinter import *
import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox, Label, Button
from datetime import datetime, timedelta
from tkcalendar import DateEntry  # importar el calendario

"""
Clase Pagos: Esta clase representa la interfaz gráfica para gestionar los pagos en una carnicería.
Contiene métodos para guardar información de pagos, actualizar el estado de los pagos y calcular el saldo pendiente.
También incluye la funcionalidad para mostrar los pagos en un Treeview y guardar la información en una base de datos SQLite.
"""

class Pagos(tk.Frame): # Hereda de tk.Frame para crear un marco en la interfaz gráfica
    db_name = "database.db"
    def __init__(self, padre):
        super().__init__(padre)
        self.deudas = []  # Lista para almacenar las deudas
        self.widgets() # Llama al método widgets para crear los elementos de la interfaz gráfica
        self.actualizar_treeview() # Llama al método para actualizar el Treeview con los datos de la base de datos

    def guardar_informacion(self): # Método para guardar la información de los pagos
        # Obtener los valores de los campos de entrada
        proveedor = self.entry_provedor.get()
        fecha_documento = self.entry_fecha_documento.get()
        factura = self.entry_factura.get()
        tipo_compra = self.combo_tipo_compra.get()  # Corregido
        fecha_vence = self.entry_fecha_vence.get()
        total_pagar = self.entry_total_pagar.get()
        monto_pagado = self.entry_monto_pagado.get()

        # Validar que todos los campos estén llenos
        if not (proveedor and fecha_documento and factura and tipo_compra and fecha_vence and total_pagar and monto_pagado):
            messagebox.showerror("Error", "Todos los campos deben estar llenos.")
            return

        # Calcular saldo pendiente
        saldo = self.saldo_pendiente(total_pagar, monto_pagado) # Llama al método para calcular el saldo pendiente
        if saldo is None:  # Si hubo un error en el cálculo, detener el proceso
            return

        # Determinar el estado
        estado = self.estado(saldo) # Llama al método para determinar el estado de la deuda

        # Agregar la deuda a la lista de deudas
        deuda = {
            "proveedor": proveedor,
            "fecha_documento": fecha_documento,
            "factura": factura,
            "tipo_compra": tipo_compra,
            "fecha_vence": fecha_vence,
            "total_pagar": total_pagar, 
            "monto_pagado": monto_pagado,
            "saldo_pendiente": saldo,
            "estado": estado
        }
        self.deudas.append(deuda) # Agrega la deuda a la lista de deudas
        messagebox.showinfo("Éxito", "Información agregada correctamente.") # Muestra un mensaje de éxito

        # Limpiar los campos de entrada
        self.entry_provedor.delete(0, END)
        self.entry_fecha_documento.delete(0, END)
        self.entry_factura.delete(0, END)
        self.combo_tipo_compra.set("")  # Corregido
        self.entry_fecha_vence.delete(0, END)
        self.entry_total_pagar.delete(0, END)
        self.entry_monto_pagado.delete(0, END)

    def actualizar_treeview(self): # Método para actualizar el Treeview con los datos de la base de datos
        # Limpiar el Treeview
        for item in self.tre.get_children(): # Itera sobre los elementos del Treeview
            self.tre.delete(item) # Elimina cada elemento

        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT proveedor, fecha_documento, factura, tipo_compra, fecha_vence, total_pagar, monto_pagado, (total_pagar - monto_pagado) AS saldo_pendiente, CASE WHEN (total_pagar - monto_pagado) > 0 THEN 'Pendiente' ELSE 'Pagado' END AS estado FROM pagos")
            registros = cursor.fetchall()
            for registro in registros:
                estado = registro[8] # Estado de la deuda
                tag_color = "rojo" if estado == "Pendiente" else "verde" # Asigna un color según el estado
                self.tre.insert("", tk.END, values=registro, tags=(tag_color,)) # Inserta los registros en el Treeview
            conn.close()      
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al cargar los datos: {e}")
       
    def guardar_en_bd(self):  # Modificado para calcular fecha_vence
        proveedor = self.entry_provedor.get() # Obtener el proveedor
        fecha_documento = self.entry_fecha_documento.get()  # Obtener la fecha del documento
        factura = self.entry_factura.get()
        tipo_compra = self.combo_tipo_compra.get() 
        total_pagar = self.entry_total_pagar.get()
        monto_pagado = self.entry_monto_pagado.get()

        if not (proveedor and fecha_documento and factura and tipo_compra and total_pagar):  # Validar que los campos necesarios estén llenos
            messagebox.showerror("Error", "Todos los campos excepto 'Monto Pagado' deben estar llenos.")
            return 

        if monto_pagado == "":  # Verificar si el campo está vacío
            monto_pagado = 0.0  # Asignar 0.0 si el campo está vacío

        try:
            total_pagar = float(total_pagar)  # Convertir a float
            monto_pagado = float(monto_pagado)  # Convertir a float
        except ValueError:
            messagebox.showerror("Error", "El monto pagado debe ser un número.")
            return

        try:
            # Calcular fecha de vencimiento si el tipo de compra es "Credito"
            if tipo_compra == "Credito":
                fecha_documento_dt = datetime.strptime(fecha_documento, "%d-%m-%Y")  # Convertir a objeto datetime
                fecha_vence_dt = fecha_documento_dt + timedelta(days=15)  # Sumar 15 días
                fecha_vence = fecha_vence_dt.strftime("%d-%m-%Y")  # Convertir de nuevo a string
            else:
                fecha_vence = fecha_documento  # Si es "Contado", la fecha de vencimiento es la misma

            # Calcular saldo pendiente y determinar estado
            saldo_pendiente = self.saldo_pendiente(total_pagar, monto_pagado)
            if saldo_pendiente is None:  # Si hubo un error en el cálculo, detener el proceso
                return
            estado, _ = self.estado(saldo_pendiente) # Llama al método para determinar el estado de la deuda

            # Conectar a la base de datos y guardar la información
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pagos (proveedor, fecha_documento, factura, tipo_compra, fecha_vence, total_pagar, monto_pagado, saldo_pendiente, estado) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (proveedor, fecha_documento, factura, tipo_compra, fecha_vence, total_pagar, monto_pagado, saldo_pendiente, estado))
            conn.commit() # Guardar los cambios en la base de datos
            messagebox.showinfo("Éxito", "Información guardada con éxito.")
            self.actualizar_treeview() # Refrescar el Treeview después de guardar
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al guardar la información: {e}")
        finally:
            conn.close()

        # Limpiar los campos de entrada después de guardar
        self.entry_provedor.delete(0, END)
        self.entry_fecha_documento.delete(0, END)
        self.entry_factura.delete(0, END)
        self.combo_tipo_compra.set("")
        self.entry_total_pagar.delete(0, END)
        self.entry_monto_pagado.delete(0, END)

    def actualizar_pago(self): # Método para actualizar el pago
        # Obtener los valores de los campos de entrada
        factura = self.entry_factura.get() # Obtener el número de factura
        monto_pagado = self.entry_monto_pagado.get()

        # Validar que los campos necesarios estén llenos
        if not (factura and monto_pagado):
            messagebox.showerror("Error", "Debe ingresar el número de factura y el monto pagado.")
            return

        try:
            monto_pagado = float(monto_pagado)  # Convertir a float
        except ValueError:
            messagebox.showerror("Error", "El monto pagado debe ser un número.")
            return

        try:
            # Conectar a la base de datos y actualizar el monto pagado
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("UPDATE pagos SET monto_pagado = ? WHERE factura = ?", (monto_pagado, factura)) # Actualizar el monto pagado en la base de datos
            conn.commit()

            if cursor.rowcount == 0:  # Verificar si se actualizó algún registro
                messagebox.showerror("Error", "No se encontró una factura con ese número.")
            else:
                messagebox.showinfo("Éxito", "Pago actualizado con éxito.")
                self.actualizar_treeview()  # Refrescar el Treeview

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al actualizar el pago: {e}")
        finally:
            conn.close()

        # Limpiar los campos de entrada
        self.entry_factura.delete(0, END) # Eliminar el número de factura
        self.entry_monto_pagado.delete(0, END) # Eliminar el monto pagado
    
    def saldo_pendiente(self, total_pagar, monto_pagado): # Método para calcular el saldo pendiente
        try:
            total_pagar = float(total_pagar) # Convertir a float
            monto_pagado = float(monto_pagado)
            #ingreso de validación: total a pagar y monto pagado no pueden ser negativos
            if total_pagar < 0 or monto_pagado < 0:  # Validar que los valores no sean negativos
                messagebox.showerror("Error", "Los valores de 'Total a Pagar' y 'Monto Pagado' no pueden ser negativos.")
                return None
            if monto_pagado > total_pagar: # Validar que el monto pagado no sea mayor que el total a pagar
                messagebox.showerror("Error", "El 'Monto Pagado' no puede ser mayor que el 'Total a Pagar'.")
                return None
            #se calcula el saldo pendiente
            saldo_pendiente = max(0,total_pagar - monto_pagado) 
            return saldo_pendiente
        except ValueError:
            messagebox.showerror("Error", "Los valores de 'Total a Pagar' y 'Monto Pagado' deben ser numéricos.")
            return None
    
    def estado(self, saldo_pendiente): # Método para determinar el estado de la deuda
        if saldo_pendiente > 0:
            return "PENDIENTE", "red" # Si hay saldo pendiente, el estado es "Pendiente"
        elif saldo_pendiente == 0:
            return "CANCELADO", "green" # Si no hay saldo pendiente, el estado es "Cancelado"
        else:
            return "Error", "black" # Si hay un error, el estado es "Error"

    def widgets(self):
        # Marco principal
        labelframe = tk.LabelFrame(self, relief="raised", borderwidth=1, bg="#477296")
        labelframe.place(x=25, y=30, width=1150, height=600)

        # Etiquetas e Ingreso de información
        titulo_label = tk.Label(labelframe, text="Pagos", font=("sans 16 bold"), bg="#477296", fg="black")
        titulo_label.place(x=10, y=10)

        label_proveedor = tk.Label(labelframe, text="Nombre Proveedor: ", font="sans 12 bold", bg="#477296")
        label_proveedor.place(x=10, y=11)
        self.entry_provedor = ttk.Entry(labelframe, font="sans 12 bold")
        self.entry_provedor.place(x=175, y=8, width=200, height=30)

        label_fecha_documento = tk.Label(labelframe, text="Fecha Documento: ", font="sans 12 bold", bg="#477296")
        label_fecha_documento.place(x=10, y=60)
        self.entry_fecha_documento = DateEntry(labelframe, font="sans 12 bold", date_pattern='dd-MM-yyyy')
        self.entry_fecha_documento.place(x=175, y=57, width=200, height=30)

        label_factura = tk.Label(labelframe, text="Número Factura: ", font="sans 12 bold", bg="#477296")
        label_factura.place(x=10, y=107)
        self.entry_factura = ttk.Entry(labelframe, font="sans 12 bold")
        self.entry_factura.place(x=175, y=107, width=200, height=30)

        label_total_pagar = tk.Label(labelframe, text="Total a Pagar", font="sans 12 bold", bg="#477296")
        label_total_pagar.place(x=450, y=11)
        self.entry_total_pagar = ttk.Entry(labelframe, font="sans 12 bold")
        self.entry_total_pagar.place(x=590, y=8, width=200, height=30)

        label_monto_pagado = tk.Label(labelframe, text="Monto Pagado: ", font="sans 12 bold", bg="#477296")
        label_monto_pagado.place(x=450, y=60)
        self.entry_monto_pagado = ttk.Entry(labelframe, font="sans 12 bold")
        self.entry_monto_pagado.place(x=590, y=58, width=200, height=30)

        # Elegir el tipo de compra de mercaderia Contado o Credito
        label_tipo_compra = tk.Label(labelframe, text="Tipo de Compra: ", font="sans 12 bold", bg="#477296")
        label_tipo_compra.place(x=450, y=107)
        opciones = ["Contado", "Credito"] # Opciones para el tipo de compra
        self.combo_tipo_compra = ttk.Combobox(labelframe, values=opciones, font="sans 12 bold") # Crear el ComboBox
        self.combo_tipo_compra.place(x=590, y=107, width=200, height=30)
       
       
        self.boton_guardar_bd = Button(self, text="Guardar en BD", font=("sans 10 bold"), command=self.guardar_en_bd)
        self.boton_guardar_bd.place(x=880, y=450, width=150, height=30)

        # Coloca el Treeview en la ventana
        treFrame = tk.Frame(self)
        treFrame.place(x=25, y=220, width=1148, height=300)

        #  para movilizarse en horizontal y en vertical
        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT, fill=Y)

        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL) 
        scrol_x.pack(side=BOTTOM, fill=X)

        # Treeview para mostrar la información de los pagos
        self.tre = ttk.Treeview(treFrame, columns=("Proveedor", "Fecha Documento", "Factura", "Tipo de Compra", "Fecha Vencimiento", "Total Pagar", "Monto Pagado", "Saldo Pendiente", "Estado"), show="headings")

        self.tre.pack(expand=True, fill=BOTH) # Expandir el Treeview para llenar el espacio disponible

        scrol_y.config(command=self.tre.yview) # Configurar el scrollbar vertical
        scrol_x.config(command=self.tre.xview) # Configurar el scrollbar horizontal
        
        self.tre.tag_configure("rojo", foreground="red") # Configurar el color rojo para las filas con saldo pendiente
        self.tre.tag_configure("verde", foreground="green") # Configurar el color verde para las filas pagadas

        # Configurar los encabezados directamente con texto
        self.tre.heading("Proveedor", text="Proveedor")
        self.tre.heading("Fecha Documento", text="Fecha Documento")
        self.tre.heading("Factura", text="Factura")
        self.tre.heading("Tipo de Compra", text="Tipo de Compra")
        self.tre.heading("Fecha Vencimiento", text="Fecha Vencimiento")
        self.tre.heading("Total Pagar", text="Total Pagar")
        self.tre.heading("Monto Pagado", text="Monto Pagado")
        self.tre.heading("Saldo Pendiente", text="Saldo Pendiente")
        self.tre.heading("Estado", text="Estado")

        # Configurar el ancho de las columnas
        self.tre.column("Proveedor", width=60)
        self.tre.column("Fecha Documento", width=50)
        self.tre.column("Factura", width=60)
        self.tre.column("Tipo de Compra", width=80)
        self.tre.column("Fecha Vencimiento", width=50)
        self.tre.column("Total Pagar", width=85)
        self.tre.column("Monto Pagado", width=85)
        self.tre.column("Saldo Pendiente", width=85)
        self.tre.column("Estado", width=80)

        self.grid_rowconfigure(0, weight=0)  # Configura el peso de la fila 0
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)  # Configura el peso de la fila 2
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)  # Configura el peso de la fila 4
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_rowconfigure(8, weight=1)
        
        # Botón para agregar información
        Button(self, text="Agregar Información",bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296" ,command=self.guardar_en_bd).place(x=880, y=38, width=150, height=30) 
        Button(self, text="Actualizar Pago",bg="white", fg="black", relief="flat", highlightthickness=1, borderwidth=0, highlightbackground="#477296" ,command=self.actualizar_pago).place(x=880, y=88, width=150, height=30)



