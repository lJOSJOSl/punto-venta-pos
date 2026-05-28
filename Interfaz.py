import tkinter as tk
from caja import Caja

caja = Caja()

#funciones

def mostrar_catalogo():

    texto.delete("1.0", tk.END)

    for producto in caja.productos:

        texto.insert(
            tk.END,
            f'{producto["nombre"]:<20} ${producto["precio"]}\n'
        )

def mostrar_ventas(event=None):

    frame_productos.pack_forget()

    frame_ventas.pack(fill="both", expand=True)

def mostrar_productos(event=None):
    
    frame_ventas.pack_forget()

    frame_productos.pack(fill="both", expand=True)

def agregar_producto():

    nombre = entrada_codigo.get()

    nombre = entrada_nombre.get()

    precio = entrada_precio.get()

    if nombre == "" or precio == "":
        print("completa todos los campos")
        return
    try:
        producto = {
            "codigo_barras": codigo_barras,
            "nombre": nombre,
            "precio": float(precio)
        }

        caja.agregar_producto_inventario(producto)
        mostrar_catalogo()
        mostrar_ventas()
    
        entrada_nombre.delete(0, tk.END)

        entrada_precio.delete(0, tk.END)
     
    except ValueError:
        print("El precio debe ser un numero")

#Ventanas

ventana = tk.Tk()

ventana.title("Punto de venta")
ventana.geometry("800x600")

barra_superior = tk.Frame(ventana)

barra_superior.pack(fill="x")

btn_ventas = tk.Button(
    barra_superior,
    text="F1 Ventas",
    command=mostrar_ventas
)
btn_ventas.pack(side="left", padx=10, pady=10)

btn_productos = tk.Button(
    barra_superior,
    text="F2 Productos",
    command=mostrar_productos
)
btn_productos.pack(side="left", padx=10, pady=10)

#Frames

frame_ventas = tk.Frame(ventana)

frame_productos = tk.Frame(ventana)

frame_ventas.pack(fill="both", expand=True)

#pantalla ventas

titulo = tk.Label(
    frame_ventas,
    text="F1 : Ventas",
    font=("Arial", 24)
)

titulo.pack(pady=20)

boton = tk.Button(
    frame_ventas,
    text = "Mostrar catálogo",
    command = mostrar_catalogo
)

boton.pack(pady=10)

texto = tk.Text(
    frame_ventas,
    height = 20,
    width = 60,
    font = ("Arial", 12)

)

texto.pack(pady=20)

#pantalla productos

titulo_productos = tk.Label(
    frame_productos,
    text="F2 : Productos",
    font=("Arial", 24)
)
titulo_productos.pack(pady=20)

frame_codigo = tk.Frame(frame_productos)
frame_codigo.pack(pady=5)

label_codigo = tk.Label(frame_codigo, text= "Codigo de barras")
label_codigo.pack(side="left", padx=5)

entrada_codigo = tk.Entry(frame_codigo, width=40)
entrada_codigo.pack(side="left")

frame_nombre = tk.Frame(frame_productos)
frame_nombre.pack(pady=5)

label_nombre = tk.Label(frame_nombre, text="Descripción")
label_nombre.pack(side="left", padx=5)

entrada_nombre = tk.Entry(frame_nombre, width=40)
entrada_nombre.pack(side="left")

frame_costo = tk.Frame(frame_productos)
frame_costo.pack(pady=5)

label_costo = tk.Label(frame_costo, text="Precio costo")
label_costo.pack(side="left", padx=5)

entrada_costo = tk.Entry(frame_costo, width=5)
entrada_costo.pack(side="left")


frame_precio = tk.Frame(frame_productos)
frame_precio.pack(pady=5)

label_precio = tk.Label(frame_precio, text="Precio")
label_precio.pack(side="left", padx=5)

entrada_precio = tk.Entry(frame_precio, width=5)
entrada_precio.pack(side="left")




btn_agregar = tk.Button(
    frame_productos,
    text= "Agregar producto",
    command=agregar_producto
)
btn_agregar.pack()

#teclas
ventana.bind("<F1>", mostrar_ventas)

ventana.bind("<F2>", mostrar_productos)
#mainloop

ventana.mainloop()
