# 🛒 Sistema de Punto de Venta (POS)

Aplicación desarrollada con Python para el funcionamiento de una caja registradora.

## 🚀 Funcionalidades

- Agregar productos al carrito      (✔)
- Carrito de compras                (✔)
- Cálculo automático de total       (✔)  
- Generación de ticket              (❌)
- Almacenamiento de ventas en JSON  (✔)
- Historial de ventas               (❌)
- Corte                             (❌)
- Usuarios                          (❌)
- Catalogo (Inventario)             (📌)

## 🧱 Estructura

- main.py → Ejecuta el programa (arranque)
- caja.py → Lógica principal del sistema funciones para agregar producto
- Interfaz.py → Gui del sistema
- producto.py → Clases para productos en inventario y productos para el carrito
- productos.json → Catálogo (almacenamiento de los productos)
- ventas.json → Historial de ventas
- utilidades.py → Funciones reutilizables

## 📸 Capturas del sistema

### Pantalla principal
![Pantalla principal](imagenes/Frame_venta.png)

### Pantalla busqueda de productos
![Pantalla busqueda f10](imagenes/Frame_busqueda.png)

### Pantalla productos agregar un nuevo producto
![Pantalla productos](imagenes/Frame_productos.png)

## ▶️ Ejecución

Abriendo el cmd/consola desde la ubicacion de la carpeta
podemos correr el programa con el siguiente comando:

python main.py