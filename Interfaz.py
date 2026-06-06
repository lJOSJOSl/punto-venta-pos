# -----------------Importaciones-----------------

import tkinter as tk
from tkinter import ttk
from caja import Caja

# -----------------Objetos globales-----------------

caja = Caja()

# -----------------Funciones-----------------

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

def agregar_al_carrito(event=None):

    codigo = entrada_codigo_venta.get()

    for producto in caja.productos:
        if producto.get("codigo_barras") == codigo:

            tabla_venta.insert("", 
                        tk.END, 
                        values=(
                        producto.get("codigo_barras",""),
                        producto.get("nombre", ""),
                        producto.get("precio_venta", 0),
                        1,
                        producto.get("precio_venta", 0),
                        "N/A"
                               )
                        )
def mostrar_ventas(event=None):

    frame_productos.grid_forget()
    frame_ventas.grid(row=1, column=0, sticky="nsew")

def mostrar_productos(event=None):

    frame_ventas.grid_forget()
    frame_productos.grid(row=1, column=0, sticky="nsew")

def abrir_busqueda(event=None):

    ventana_busqueda = tk.Toplevel(ventana)
    ventana_busqueda.title("Busqueda de Productos")
    ventana_busqueda.geometry("700x500")

    tabla = ttk.Treeview(
        ventana_busqueda,
        columns=("nombre", "precio_venta","departamento"),
        show="headings"
    )

    
# ---ENCABEZADOS---

    tabla.heading("nombre", text="Producto")
    tabla.heading("precio_venta", text="Precio")
    tabla.heading("departamento", text="Departamento")

# ---Ancho de columnas---

    tabla.column("nombre", width=300)
    tabla.column("precio_venta", width=100)
    tabla.column("departamento", width=150)
   
    entrada = tk.Entry(
        ventana_busqueda,
        font=("Arial", 16),
        width=40
    )

    entrada.pack(pady=10)
    tabla.pack(fill="both", expand=True)
    
    print("Productos en caja:", caja.productos)

    def buscar(event=None):
    
        tabla.delete(*tabla.get_children())

        texto = entrada.get().strip().lower()
        
        print("Buscando:", texto)#Debug

        for producto in caja.productos:

            nombre = producto.get("nombre", "").lower()

            if texto == "" or texto in nombre:

                tabla.insert(
                     "",
                     tk.END,
                     values=(
                         producto.get("nombre", ""),
                         producto.get("precio_venta", 0),
                         producto.get("departamento", "")
                     )
                )

    entrada.bind("<KeyRelease>", buscar)

    def seleccionar(event=None):
        
        item = tabla.focus()

        if not item:
            return

        valores = tabla.item(item, "values")

        tabla_venta.insert(
            "",
            tk.END,
            values=(
                "",
                valores[0],
                valores[1],
                1,
                valores[1],
            )
        )

        ventana_busqueda.destroy()
    
    tabla.bind("<Return>", seleccionar)

    entrada.focus_set()


#-----------------Ventanas-----------------

# ---VENTANA PRINCIPAL---

ventana = tk.Tk()

ventana.title("Punto de venta")
ventana.geometry("800x600")

ventana.grid_rowconfigure(1, weight=1)
ventana.grid_columnconfigure(0, weight=1)

#-------------Frame superior-------------

frame_header = tk.Frame(ventana, height=80, relief="ridge", bd=2)
frame_header.grid(row=0, column=0, sticky="ew")

# --- Logo ---

label_logo = tk.Label(frame_header, text="LOGO", width=10)
label_logo.grid(row=0, column=0, rowspan=2, padx=10)

# --- Giro ---

label_giro = tk.Label(frame_header, text="Giro", font=("Arial", 18, "bold"))
label_giro.grid(row=0, column=1, sticky="w")

# --- Nombre negocio ---

label_nombre = tk.Label(frame_header, text="Nombre", font=("Arial", 18, "bold"))
label_nombre.grid(row=1, column=1, sticky="w")

frame_header.columnconfigure(1, weight=1)

# --- Boton usuario ---

btn_usuario = tk.Button(frame_header, text="usuario", width=3)
btn_usuario.grid(row=1, column=2, rowspan=2, padx=10)

#-------------barra botones/funciones-------------

barra_funciones = tk.Frame(ventana)
barra_funciones.grid(row=1, column=0, sticky="ew")

#-----------------Frames-----------------
# --- F1 Ventas ---

frame_ventas = tk.Frame(ventana)
frame_ventas.grid(row=2, column=0, sticky="nsew")

# --- Expansion interna ---

frame_ventas.grid_rowconfigure(2, weight=1)
frame_ventas.grid_columnconfigure(0, weight=1)

# --- Titulo ---

titulo_ventas = tk.Label(frame_ventas, text="F1 : Ventas", font=("Arial", 24))
titulo_ventas.grid(row=0, column=0, pady=10)

# --- Captura codigo ---

frame_codigo_venta = tk.Frame(frame_ventas)
frame_codigo_venta.grid(row=1, column=0, sticky="nsew")

label_codigo_venta = tk.Label(frame_codigo_venta, text= "Codigo del Producto:")
label_codigo_venta.pack(side="left", padx=5)

entrada_codigo_venta = tk.Entry(frame_codigo_venta, width=30, font=("Arial", 18))
entrada_codigo_venta.pack(side="left")

entrada_codigo_venta.bind("<Return>", agregar_al_carrito)


# !--- Tabla carrito en F1 ---!

tabla_venta = ttk.Treeview(
    frame_ventas,
    columns =(
        "codigo",
        "descripcion",
        "precio",
        "cantidad",
        "importe"
        ),
        show="headings",
    )

# !---Encabezados---!

tabla_venta.heading("codigo", text="Codigo")
tabla_venta.heading("descripcion", text="Descripción")
tabla_venta.heading("precio", text="Precio")
tabla_venta.heading("cantidad", text="Cantidad")
tabla_venta.heading("importe", text="Importe")

# !---Ancho de columnas---!

tabla_venta.column("codigo", width=150)
tabla_venta.column("descripcion", width=300)
tabla_venta.column("precio", width=100)
tabla_venta.column("cantidad", width=80)
tabla_venta.column("importe", width=100)

# --- Mostrar tabla ---

tabla_venta.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

# !--- Frame total inferior ---!

frame_total = tk.Frame(frame_ventas)
frame_total.grid(row=4, column=0, sticky="ew")

label_total = tk.Label(frame_total, text="TOTAL: $0.00", font=("Arial", 22, "bold"))
label_total.pack(side="right", padx=20, pady=10)

#-----------------pantalla ventas-----------------

btn_ventas = tk.Button(
    barra_funciones,
    text="F1 Ventas",
    command=mostrar_ventas
)
btn_ventas.pack(side="left", padx=10, pady=10)

btn_productos = tk.Button(
    barra_funciones,
    text="F2 Productos",
    command=mostrar_productos
)
btn_productos.pack(side="left", padx=10, pady=10)


#-----------------pantalla productos-----------------

frame_productos = tk.Frame(ventana)

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
ventana.bind("<F10>", abrir_busqueda)

#Mainloop
ventana.mainloop()