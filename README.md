# Sistema de Punto de Venta - Carnicería El Asadito

## Descripción

Sistema integral de gestión y punto de venta para una carnicería, desarrollado en **Python 3.13+** utilizando **Tkinter** como interfaz gráfica. Incluye funcionalidades de inventario, gestión de clientes, proveedores, pagos y generación de reportes en PDF.

## Características Principales

- **Autenticación de Usuarios**: Sistema de login y registro de usuarios
- **Gestión de Productos**: Registro, edición y eliminación de productos con imágenes
- **Inventario**: Control de almacén con alertas de stock bajo
- **Clientes**: Base de datos de clientes y registro de compras
- **Proveedores**: Gestión de proveedores y órdenes de compra
- **Punto de Venta**: Interfaz de ventas con carrito de compras
- **Pagos**: Registro de pagos y métodos de pago
- **Pedidos**: Gestión de pedidos de clientes
- **Caja**: Cierre de caja diario y reportes financieros
- **Reportes**: Generación de reportes en PDF con ReportLab
- **Información**: Datos de la empresa y funcionalidades adicionales

## Requisitos

- **Python**: 3.13.2 o superior
- **Sistema Operativo**: Windows, macOS o Linux

## Dependencias

Las siguientes librerías se instalarán automáticamente:

```
Pillow>=9.0.0      # Procesamiento de imágenes
tkcalendar>=1.6.0  # Widget de calendario para Tkinter
reportlab>=3.6.0   # Generación de reportes PDF
```

## Instalación

### 1. Clonar o descargar el proyecto

```bash
git clone https://github.com/marcos85-cr/Punto-Venta-Carniceria-Python-Tkinter.git
cd Punto-Venta-Carniceria-Python-Tkinter
```

### 2. Crear un entorno virtual (recomendado)

```bash
python -m venv .venv
```

**Activar el entorno virtual:**

- **Windows**:
  ```bash
  .venv\Scripts\activate
  ```

- **macOS/Linux**:
  ```bash
  source .venv/bin/activate
  ```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```bash
cd CARNICERIA
python index.py
```

## Estructura del Proyecto

```
Punto-Venta-Carniceria-Python-Tkinter/
├── CARNICERIA/
│   ├── index.py              # Punto de entrada de la aplicación
│   ├── manager.py            # Gestor principal de ventanas
│   ├── login.py              # Autenticación de usuarios
│   ├── container.py          # Contenedor principal de la aplicación
│   ├── productos.py          # Gestión de productos
│   ├── almacen.py            # Control de inventario
│   ├── clientes.py           # Gestión de clientes
│   ├── proveedor.py          # Gestión de proveedores
│   ├── pagos.py              # Procesamiento de pagos
│   ├── pedidos.py            # Gestión de pedidos
│   ├── caja.py               # Cierre de caja y reportes
│   ├── punto_venta.py        # Interfaz de ventas
│   ├── informacion.py        # Información de la empresa
│   ├── iconos/               # Iconos de la interfaz
│   ├── imagenes/             # Imágenes estáticas
│   ├── fotos/                # Fotos de productos
│   ├── cierres_caja/         # Reportes de cierre (generados)
│   ├── facturas/             # PDFs de facturas (generados)
│   └── informes/             # Reportes financieros (generados)
├── .gitignore                # Configuración de Git
├── README.md                 # Este archivo
└── CARNICERIA.code-workspace # Configuración de VS Code
```

## Uso

### Iniciar sesión

1. Ejecuta `python index.py` en la carpeta CARNICERIA
2. Usa las credenciales de login o crea una nueva cuenta
3. Accede al panel principal de la aplicación

### Operaciones Principales

- **Vender productos**: Usa la sección "Punto de Venta" para registrar ventas
- **Gestionar inventario**: Accede a "Almacén" para ver stock disponible
- **Registrar clientes**: Añade nuevos clientes en la sección "Clientes"
- **Consultar proveedores**: Gestiona proveedores y órdenes de compra
- **Generar reportes**: Crea reportes PDF desde "Caja" e "Informes"

## Tecnologías Utilizadas

- **Python 3.13.2**
- **Tkinter** - Interfaz gráfica
- **SQLite** - Base de datos local
- **Pillow** - Procesamiento de imágenes
- **tkcalendar** - Widget de calendario
- **ReportLab** - Generación de PDF

## Notas de Desarrollo

- La aplicación utiliza SQLite para almacenamiento de datos (archivos `.db`)
- Las imágenes de productos se almacenan en la carpeta `fotos/`
- Los reportes generados se guardan en las carpetas `cierres_caja/`, `facturas/` e `informes/`
- El proyecto está configurado para trabajar con un entorno virtual en `.venv/`

## Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Autor

**Marcos Vargas Hernández**

- Fecha de inicio: 14-04-2025
- IDE: Visual Studio Code
- Versión actual: 1.0

## Soporte

Si encuentras problemas o tienes sugerencias, por favor abre un issue en el repositorio.

---

**Última actualización**: Junio 2026
