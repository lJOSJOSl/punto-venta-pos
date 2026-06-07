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
    print("Escaneado:", entrada_codigo_venta.get())

    codigo = entrada_codigo_venta.get().strip()

    producto = caja.agregar_producto_carrito(codigo)

    actualizar_tabla()

    if producto is None:
        return

    print("CONTENIDO:", repr(entrada_codigo_venta.get()))
    entrada_codigo_venta.delete(0, tk.END)
    print("DESPUES:", repr(entrada_codigo_venta.get()))
    entrada_codigo_venta.focus_set()
    return "break"

def aumentar_cantidad(event=None):

    item = tabla_venta.focus()
    if not item:
        return
    codigo = tabla_venta.item(item, "values")[0]
    caja.aumentar_cantidad(codigo)

    actualizar_tabla()

def disminuir_cantidad(event=None):

    item = tabla_venta.focus()
    if not item:
        return
    codigo = tabla_venta.item(item, "values")[0]
    caja.disminuir_cantidad(codigo)

    actualizar_tabla()

def mostrar_ventas(event=None):

    frame_productos.grid_forget()
    frame_ventas.grid(row=2, column=0, sticky="nsew")

def mostrar_productos(event=None):

    frame_ventas.grid_forget()
    frame_productos.grid(row=2, column=0, sticky="nsew")

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


def actualizar_tabla():

    tabla_venta.delete(*tabla_venta.get_children())

    total = 0
 
    for producto in caja.carrito:
        
        importe = producto.precio * producto.cantidad
        total += importe
        
        tabla_venta.insert("", "end", values=(producto.codigo, producto.nombre, producto.precio, producto.cantidad, importe))

    label_total.config(text=f"${total:,.2f}")

    cantidad_articulos = sum(producto.cantidad for producto in caja.carrito)

    label_articulos.config(text=f"{cantidad_articulos} Articulos en la venta actual")

    label_total_grande.config(text=f"${total:,.2f}")
    
    

#-----------------Ventanas-----------------

# ---VENTANA PRINCIPAL---

ventana = tk.Tk()

ventana.title("Punto de venta")
ventana.state("zoomed")

ventana.grid_rowconfigure(3, weight=1)
ventana.grid_columnconfigure(0, weight=1)

#-------------Frame superior-------------

frame_header = tk.Frame(ventana, height=40, relief="ridge", bd=2)
frame_header.grid(row=0, column=0, sticky="ew", pady=(0,2))

# --- Logo ---

label_logo = tk.Label(frame_header, text="LOGO", width=10)
label_logo.grid(row=0, column=0, rowspan=2, padx=10)

# --- Giro ---

label_giro = tk.Label(frame_header, text="Giro", font=("Arial", 10, "bold"))
label_giro.grid(row=0, column=1, sticky="w")

# --- Nombre negocio ---

label_nombre = tk.Label(frame_header, text="Nombre", font=("Arial", 10, "bold"))
label_nombre.grid(row=1, column=1, sticky="w")

frame_header.columnconfigure(1, weight=1)

# --- Boton usuario ---

btn_usuario = tk.Button(frame_header, text="usuario", width=8)
btn_usuario.grid(row=0, column=2, rowspan=2, padx=10)

#-------------barra botones/funciones-------------

barra_funciones = tk.Frame(ventana, height=30, relief="ridge", bd=2)
barra_funciones.grid(row=1, column=0, sticky="ew")

#-----------------Frames-----------------
# --- F1 Ventas ---

frame_ventas = tk.Frame(ventana)
frame_ventas.grid(row=2, column=0, sticky="nsew")

# --- Expansion interna ---

frame_ventas.grid_rowconfigure(3, weight=1)
frame_ventas.grid_columnconfigure(0, weight=1)

# --- Titulo ---

titulo_ventas = tk.Label(frame_ventas, text="Venta de productos", font=("Arial", 10), relief="ridge", bd=2)
titulo_ventas.grid(row=0, column=0, sticky="w", pady=2)

# --- Captura codigo ---

frame_codigo_venta = tk.Frame(frame_ventas)
frame_codigo_venta.grid(row=1, column=0, sticky="nsew", pady=(2,2))

label_codigo_venta = tk.Label(frame_codigo_venta, text= "Codigo del Producto:")
label_codigo_venta.pack(side="left", padx=5)

entrada_codigo_venta = tk.Entry(frame_codigo_venta, width=30, font=("Arial", 18))
entrada_codigo_venta.pack(side="left")

btn_enter = tk.Button(frame_codigo_venta, text="Enter - agregar producto", command=agregar_al_carrito)
btn_enter.pack(side="left")

entrada_codigo_venta.bind("<Return>", agregar_al_carrito)

frame_codigo_venta.columnconfigure(0, weight=1)

# --- Botones para venta ---

frame_botones_ventas = tk.Frame(frame_ventas)
frame_botones_ventas.grid(row=2, column=0, sticky="w", pady=(2,2))

btn_venta_rapida = tk.Button(frame_botones_ventas, text="CTRL+P VR",)
btn_venta_rapida.pack(side="left")

btn_buscar = tk.Button(frame_botones_ventas, text="F10: Buscar", command=abrir_busqueda)
btn_buscar.pack(side="left")

btn_entradas = tk.Button(frame_botones_ventas, text="F4 Entradas")
btn_entradas.pack(side="left")

btn_salidas = tk.Button(frame_botones_ventas, text="F5 Salidas")
btn_salidas.pack(side="left")

btn_borrar_articulo = tk.Button(frame_botones_ventas, text="Borrar Articulo")
btn_borrar_articulo.pack(side="left")


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
        height=20
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

tabla_venta.grid(row=3, column=0, sticky="nsew",padx=10, pady=2)

# !--- Frame total inferior ---!

frame_total = tk.Frame(frame_ventas)
frame_total.grid(row=4, column=0, sticky="ew")

label_articulos = tk.Label(frame_total, text="0 productos en la venta actual", font=("Arial", 14))
label_articulos.pack(side="left", padx=20)

label_total_grande = tk.Label(frame_total, text="$0.00", font=("Arial", 22, "bold"))
label_total_grande.pack(side="right", padx=10, pady=2)

btn_cobrar = tk.Button(frame_total, text="F12 Cobrar", font=("Arial", 14, "bold"))
btn_cobrar.pack(side="right", padx=10, pady=2)

# !--- Frame pago ---!

frame_pago = tk.Frame(frame_ventas)
frame_pago.grid(row=5, column=0, sticky="ew")

label_total = tk.Label(frame_pago, text="Total: $0.00", font=("Arial", 12))
label_total.pack(side="left")

label_pago = tk.Label(frame_pago, text="Pago con: $0.00", font=("Arial", 12))
label_pago.pack(side="left")

label_cambio = tk.Label(frame_pago, text="Cambio: $0.00", font=("Arial", 12)) 
label_cambio.pack(side="left")


# ! --- Frame Info ---- !

frame_info = tk.Frame(frame_ventas, relief="sunken", bd=1)
frame_info.grid(row=6, column=0, sticky="ew")

label_info = tk.Label(frame_info, text="Punto de venta: Teclee o escanee el producto", anchor="w")
label_info.pack(side="left", padx=2)

label_hora = tk.Label(frame_info, text="")
label_hora.pack(side="right", padx=2)


#-----------------pantalla ventas-----------------

btn_ventas = tk.Button(
    barra_funciones,
    text="F1 Ventas",
    command=mostrar_ventas
)
btn_ventas.pack(side="left", padx=10, pady=2)

btn_productos = tk.Button(
    barra_funciones,
    text="F2 Productos",
    command=mostrar_productos
)
btn_productos.pack(side="left", padx=10, pady=2)


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
ventana.bind("+", aumentar_cantidad)
ventana.bind("-", disminuir_cantidad)

ventana.bind("<F1>", mostrar_ventas)
ventana.bind("<F2>", mostrar_productos)
ventana.bind("<F10>", abrir_busqueda)

entrada_codigo_venta.focus_set()

#Mainloop
ventana.mainloop()