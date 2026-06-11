from producto import *
from datetime import datetime
import json
import os

class Caja:

    def __init__(self):

        self.inventario = self.cargar_productos()
        self.carrito = []
        self.total = 0
        self.ventas = self.cargar_ventas()

    def cargar_productos(self):

        if not os.path.exists("productos.json"):
            with open("productos.json", "w") as f:
                json.dump([], f)

        with open('productos.json', 'r') as f:
                return json.load(f)

    def guardar_productos(self):
        
        with open("productos.json", "w") as archivo:
            json.dump(self.inventario, archivo, indent=4)

    def agregar_al_carrito(self, codigo):

        for producto in self.inventario:

            if producto["codigo_barras"] == codigo:
            
                nuevo = ProductoCarrito(
                    producto["codigo_barras"],
                    producto["nombre"],
                    producto["precio_venta"]
                )
                self.carrito.append(nuevo)

                return True

        return False
 
    def aumentar_cantidad(self, codigo):

        for producto in self.carrito:
            if producto.codigo == codigo:
                producto.cantidad += 1
                return True
        return False

    def disminuir_cantidad(self, codigo):

        for producto in self.carrito:
            if producto.codigo == codigo:
                producto.cantidad -= 1
                if producto.cantidad <=0:
                    self.carrito.remove(producto)
                return True
        return False

    def eliminar_producto(self, codigo):

        for item in self.carrito:
            
            if item.codigo == codigo:
                            
                self.carrito.remove(item)
                return True

        return False

    def agregar_producto_inventario(self, codigo, nombre, venta, costo, precio,
                                    mayoreo, departamento):

        producto = ProductoInventario(codigo, nombre, venta, float(costo),
                                      float(precio), float(mayoreo), departamento)
        
        self.inventario.append(producto.to_dict())

        self.guardar_productos()

    def cantidad_articulos(self):
    
        return sum(producto.cantidad for producto in self.carrito)

    def buscar_productos_nombre(self, texto):
        
        texto = texto.lower().strip()

        if not texto:
            return []
        
        resultados = []

        for producto in self.inventario:
        
            nombre = producto.get("nombre", "").lower()
        
            if texto in nombre:
                resultados.append(producto)
        
        return resultados

    def mostrar_carrito(self):        #	Muestra productos

        if not self.carrito:
            print("Carrito vacio")
            return
        
        print("\nCarrito:")
        print("No.\tProducto\tPrecio\tCantidad\tTotal")
        print("-" * 60)
        
        for i, producto in enumerate(self.carrito, start=1):
            total_producto = producto.precio * producto.cantidad
            print(f"{i}\t{producto.nombre}\t${producto.precio:.2f}\t{producto.cantidad}\t\t${total_producto:.2f}")
            
        print("-" * 60)
        print(f"\t\t\t\tTotal: ${self.total:.2f}")

    def calcular_total(self):                 # Suma los precios

        self.total = sum(p.precio * p.cantidad for p in self.carrito)
        print(f'Total a pagar: ${self.total:.2f}')
        return self.total

    def venta(self):
        if not self.carrito:
            print("Carrito vacío")
            return

        self.calcular_total()

        try:
            monto = float(input("Dinero recibido: "))
        except ValueError:
            print("Monto inválido")
            return

        if monto < self.total:
            print(f"Dinero insuficiente")
            return
        cambio = monto - self.total
        print(f'Cambio: ${cambio:.2f}')

        confirmar = input("¿Confirmar venta? (s/n): ")

        if confirmar.lower() == 's':

            self.guardar_venta()
            self.imprimir_ticket(monto,cambio)
            print("Venta guardada")
            self.carrito.clear()
        else:

            print("Venta cancelada")

    def mostrar_catalogo(self):

        print("\n--- Catálogo ---")
        for p in self.productos:
            print(f'{p["nombre"]} - ${p["precio"]}')

    def imprimir_ticket(self, monto, cambio):

        with open("ticket.txt", "w") as f:
            f.write("------ TICKET DE COMPRA ------\n")
            f.write(f"Fecha: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}\n")
            f.write("------------------------------\n")

            for producto in self.carrito:
                total_producto = producto.precio * producto.cantidad
                f.write(f"{producto.nombre} x{producto.cantidad}  ${total_producto:.2f}\n")

            f.write("------------------------------\n")
            f.write(f"TOTAL: ${self.total:.2f}\n")
            f.write(f"RECIBIDO: ${monto:.2f}\n")
            f.write(f"CAMBIO: ${cambio:.2f}\n")
            f.write("------------------------------\n")
            f.write("Gracias por su compra\n")

    def cargar_ventas(self):

        try:
            with open('ventas.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def guardar_venta(self):

        venta = {
            'fecha' : datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            'productos' : [
                {'nombre' : p.nombre, 'precio' : p.precio, 'cantidad' : p.cantidad} 
                for p in self.carrito
            ],
            'total' : self.total
        }

        self.ventas.append(venta)

        with open('ventas.json', 'w') as f:
            json.dump(self.ventas, f, indent=4)
    
    def mostrar_ventas(self):

        if not self.ventas:
            print("No hay ventas registradas")
            return
        
        for v in self.ventas:
            print(f"\nFecha: {v['fecha']}")
            for p in v['productos']:
                print(f"- {p['nombre']} x{p['cantidad']} ${p['precio']}")        
            print(f"Total: ${v['total']}")