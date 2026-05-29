import tkinter as tk
from tkinter import ttk
from caja import Caja

caja = Caja()

#funciones

def busqueda(event=None):

    for item in tabla_venta.get_children():
        tabla_venta.delete(item)
    
    texto_busqueda = entrada_busqueda.get().lower()

    for producto in caja.productos:

        nombre = producto.get("nombre", "").lower()

        if texto_busqueda in nombre:

            tabla_venta.insert(
                "",
                tk.END,
                values=(
                    producto.get("codigo_barras", ""),
                    producto.get("nombre", ""),
                    producto.get("precio_venta", 0),
                    1,
                    producto.get("precio_venta", 0),
                    "N/A"
                )
            )

def mostrar_ventas(event=None):

    frame_productos.pack_forget()

    frame_ventas.pack(fill="both", expand=True)

def mostrar_productos(event=None):
    
    frame_ventas.pack_forget()

    frame_productos.pack(fill="both", expand=True)

def agregar_producto():

    codigo = entrada_codigo.get()

    nombre = entrada_nombre.get()

    venta = tipo_venta.get()

    costo = entrada_costo.get()

    precio = entrada_precio.get()

    mayoreo = entrada_mayoreo.get()

    departamento = combo_departamento.get()


    if nombre == "" or precio == "":
        print("completa todos los campos")
        return
    try:
        producto = {
            "codigo_barras" : codigo,
            "nombre" : nombre,
            "tipo_venta" : venta,
            "precio_costo" : float(costo),
            "precio_venta" : float(precio),
            "precio_mayoreo" : float(mayoreo),
            "departamento" : departamento
        }

        caja.agregar_producto_inventario(producto)
        busqueda()
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

frame_busqueda = tk.Frame(frame_ventas)
frame_busqueda.pack(pady=10)

label_busqueda = tk.Label(frame_busqueda, text="Buscar producto:")
label_busqueda.pack(side="left", padx=5)

entrada_busqueda = tk.Entry(frame_busqueda, width=40, font=("Arial", 14))
entrada_busqueda.pack(side="left")


tabla_venta = ttk.Treeview(
    frame_ventas,
    columns=("codigo", "descripcion", "precio", "cant", "import", "exist"),
    show = "headings",
    height = 15
)


tabla_venta.heading("codigo", text="Codigo de barras")
tabla_venta.heading("descripcion", text="Descripcion del producto")
tabla_venta.heading("precio", text="Precio venta")
tabla_venta.heading("cant", text="Cantidad")
tabla_venta.heading("import", text="Importe")
tabla_venta.heading("exist", text="Existencias")

tabla_venta.column("codigo", width=200)
tabla_venta.column("descripcion", width=200)
tabla_venta.column("precio", width=200)
tabla_venta.column("cant", width=200)
tabla_venta.column("import", width=200)
tabla_venta.column("exist", width=200)

tabla_venta.pack(pady=20)

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

frame_tipo = tk.Frame(frame_productos)
frame_tipo.pack(pady=5)

label_tipo = tk.Label(frame_tipo, text="Se vende")
label_tipo.pack(side="left")
tipo_venta = tk.StringVar()

tipo_venta.set("unidad")

radio_unidad = tk.Radiobutton(frame_tipo, text="Por unidad/pza", variable=tipo_venta, value="unidad")

radio_granel = tk.Radiobutton(frame_tipo, text="A granel(usa decimales)", variable=tipo_venta, value="granel")

radio_kit = tk.Radiobutton(frame_tipo, text="Como paquete(Kit)", variable=tipo_venta, value="kit")

radio_unidad.pack(side="left")
radio_granel.pack(side="left")
radio_kit.pack(side="left")

frame_costo = tk.Frame(frame_productos)
frame_costo.pack(pady=5)

label_costo = tk.Label(frame_costo, text="Precio costo")
label_costo.pack(side="left", padx=5)

entrada_costo = tk.Entry(frame_costo, width=5)
entrada_costo.pack(side="left")


frame_precio = tk.Frame(frame_productos)
frame_precio.pack(pady=5)

label_precio = tk.Label(frame_precio, text="Precio venta")
label_precio.pack(side="left", padx=5)

entrada_precio = tk.Entry(frame_precio, width=5)
entrada_precio.pack(side="left")

frame_mayoreo = tk.Frame(frame_productos)
frame_mayoreo.pack(pady=5)

label_mayoreo = tk.Label(frame_mayoreo, text="Precio mayoreo")
label_mayoreo.pack(side="left", padx=5)

entrada_mayoreo = tk.Entry(frame_mayoreo, width=5)
entrada_mayoreo.pack(side="left")

frame_departamento = tk.Frame(frame_productos)
frame_departamento.pack(pady=5)

label_departamento = tk.Label(frame_departamento, text="Departamento")
label_departamento.pack(side="left")

combo_departamento = ttk.Combobox(frame_departamento, values=["Abarrotes","Bimbo","Lala", "Coca cola"])
combo_departamento.set("Abarrotes")
combo_departamento.pack(side="left")


btn_agregar = tk.Button(
    frame_productos,
    text= "Agregar producto",
    command=agregar_producto
)
btn_agregar.pack()

#teclas
ventana.bind("<F1>", mostrar_ventas)

ventana.bind("<F2>", mostrar_productos)

ventana.bind("<F10>", busqueda)
#mainloop

ventana.mainloop()
