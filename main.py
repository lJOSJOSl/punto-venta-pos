from caja import Caja

def main():         # Ejecuta el menu y programa principal

    caja = Caja()

    opciones = {
        "1" : caja.agregar_producto,
        "2" : caja.mostrar_carrito,
        "3" : caja.calcular_total,
        "4" : caja.eliminar_producto,
        "5" : caja.venta,
        "6" : caja.mostrar_ventas,
        "7" : exit
    }
    while True:
        print("\n--- CAJA REGISTRADORA ---")
        print("1. Agregar producto")
        print("2. Mostrar carrito")
        print("3. Calcular total")
        print("4. Eliminar producto")
        print("5. Venta")
        print("6. Mostrar ventas")
        print("7. Salir")
        opcion = input("Elige una opción: ")
        if opcion in opciones:
            opciones[opcion]()
        else:
            print("opción invalida")
if __name__ == "__main__":        
    main()