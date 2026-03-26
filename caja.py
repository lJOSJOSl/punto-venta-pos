from producto import Producto
from datetime import datetime
import json

class Caja:
    def __init__(self):
        self.carrito = []
        self.total = 0
        self.ventas = self.cargar_ventas()
        self.productos = self.cargar_productos()

    def cargar_productos(self):
        try:
            with open('productos.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def agregar_producto(self):      # Agrega productos
        self.mostrar_catalogo()
        
        if not self.productos:
            print("No hay productos disponibles")
            return

        nombre = input("Nombre del producto: ").lower()
        
        producto_encontrado = None
        for p in self.productos:
            if p["nombre"].lower() == nombre:
                producto_encontrado = p
                break

        if not producto_encontrado:
            print("Producto no encontrado")
            return

        print(f'Producto: {producto_encontrado["nombre"]} - ${producto_encontrado["precio"]}')

        while True:
            try:
                cantidad = int(input("Cantidad: "))
                if cantidad <= 0:
                    print("Debe ser mayor a 0")
                else:
                    break
            except ValueError:
                print("Valor invalido")
        
        producto = Producto(
            producto_encontrado["nombre"],
            producto_encontrado["precio"],
            cantidad
        )
        
        self.carrito.append(producto)
        print("Producto agregado")


    def mostrar_carrito(self):        #	Muestra productos
        if not self.carrito:
            print("Carrito vacio")
            return
        self.calcular_total()
        
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

    def eliminar_producto(self):
        self.mostrar_carrito()
        
        try:
            indice = int(input("numero de producto a eliminar: ")) -1
            if 0 <= indice < len(self.carrito):
                self.carrito.pop(indice)
                self.calcular_total()
                print("Producto eliminado")
            else:
                print("Indice inválido")
        except ValueError:
            print("Entrada invalida")
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