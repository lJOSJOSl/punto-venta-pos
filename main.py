from caja import Caja

def main():         # Ejecuta el menu y programa principal

    caja = Caja()

    opciones = {
        "1" : caja.agregar_producto_carrito,
        "2" : caja.agregar_producto_inventario,
        "3" : caja.mostrar_carrito,
        "4" : caja.calcular_total,
        "5" : caja.eliminar_producto,
        "6" : caja.venta,
        "7" : caja.mostrar_ventas,
        "8" : exit,
        "9" : caja.mostrar_catalogo
    }
    while True:
        print("\n--- CAJA REGISTRADORA ---")
        print("1. Agregar producto al carrito")
        print("2. Agregar producto al inventario")
        print("3. Mostrar carrito")
        print("4. Calcular total")
        print("5. Eliminar producto")
        print("6. Venta")
        print("7. Mostrar ventas")
        print("8. Salir")
        print("9. Mostrar catalogo")
        opcion = input("Elige una opción: ")
        if opcion in opciones:
            opciones[opcion]()
        else:
            print("opción invalida")
if __name__ == "__main__":        
    main()