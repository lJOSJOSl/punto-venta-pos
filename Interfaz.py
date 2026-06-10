# -----------------Importaciones-----------------

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from utilidades import *
from caja import Caja

# -----------------Objetos globales-----------------

caja = Caja()
codigo_seleccionado = None

# -----------------Funciones-----------------

def agregar_producto():

    codigo = entrada_codigo.get()
    nombre = entrada_nombre.get()
    venta = tipo_venta.get()
    costo = entrada_costo.get()
    precio = entrada_precio.get()
    mayoreo = entrada_mayoreo.get()
    departamento = combo_departamento.get()

    try:
        caja.agregar_producto_inventario(
            codigo,
            nombre,
            venta,
            costo,
            precio,
            mayoreo,
            departamento
        )

#       busqueda()
        mostrar_ventas()

        entrada_nombre.delete(0, tk.END)
        entrada_precio.delete(0, tk.END)

    except ValueError:
        print("El precio debe ser un numero")

def agregar_al_carrito(event=None):

    codigo = entrada_codigo_venta.get().strip()

    seleccionar_producto(codigo)  
    producto = caja.agregar_al_carrito(codigo)

    if producto is None:
        entrada_codigo_venta.delete(0, tk.END)
        return

    actualizar_tabla(codigo)
    
    seleccionar_producto(codigo)

    entrada_codigo_venta.delete(0, tk.END)    
    entrada_codigo_venta.focus_set()
    return "break"

def actualizar_tabla(codigo_seleccionado=None):

    tabla_venta.delete(*tabla_venta.get_children())

    total = 0
 
    for producto in caja.carrito:
        
        importe = producto.precio * producto.cantidad
        total += importe
        
        tabla_venta.insert(
             "",
             "end",
             values=(
                 producto.codigo,
                 producto.nombre,
                 f"${producto.precio:.2f}",
                 producto.cantidad, 
                 f"${importe:.2f}",
              )
           )

    if codigo_seleccionado:
    
        seleccionar_producto(codigo_seleccionado)

    elif tabla_venta.get_children():
        primer_item = tabla_venta.get_children()[0]

        tabla_venta.selection_set(primer_item)
        tabla_venta.focus(primer_item)    

    label_total.config(text=f"${total:,.2f}")

    cantidad_articulos = sum(producto.cantidad for producto in caja.carrito)

    label_articulos.config(text=f"{cantidad_articulos} Articulos en la venta actual")

    label_total_grande.config(text=f"${total:,.2f}")

def aumentar_cantidad(event=None):

    global codigo_seleccionado

    if not codigo_seleccionado:
        return "break"

    caja.aumentar_cantidad(codigo_seleccionado)

    actualizar_tabla(codigo_seleccionado)
    return "break"

def disminuir_cantidad(event=None):
    
    global codigo_seleccionado

    if not codigo_seleccionado:
        return "break"

    caja.disminuir_cantidad(codigo_seleccionado)

    actualizar_tabla(codigo_seleccionado)
    return "break"

def eliminar_producto(event=None):

    global codigo_seleccionado

    if not codigo_seleccionado:
        return "break"
    
    confirmar = messagebox.askyesno("Eliminar producto", "¿Seguro que quiere eliminar el articulo?")
    
    if confirmar:
        
        caja.eliminar_producto(codigo_seleccionado)
        
        actualizar_tabla()
        
        items = tabla_venta.get_children()
        if items:
            
            primer_item = items[0]
            valores = tabla_venta.item(primer_item, "values")
            codigo_seleccionado = valores[0]

            tabla_venta.selection_set(primer_item)
            tabla_venta.focus(primer_item)
        entrada_codigo_venta.focus_set()
    return "break"    

def seleccionar_producto(codigo):

    global codigo_seleccionado
    
    codigo_seleccionado = codigo
    
    for item in tabla_venta.get_children():

        valores = tabla_venta.item(item, "values")
            
        if str(valores[0]) == str(codigo):

            tabla_venta.focus(item)
            tabla_venta.selection_set(item)
            tabla_venta.see(item)
            break

def mostrar_ventas(event=None):

    frame_productos.grid_forget()
    frame_ventas.grid(row=2, column=0, sticky="nsew")

def mostrar_productos(event=None):

    frame_ventas.grid_forget()
    frame_productos.grid(row=2, column=0, sticky="nsew")

def abrir_busqueda(event=None):

    ventana_busqueda = tk.Toplevel(ventana)
    ventana_busqueda.grab_set()
    centrar_ventana(ventana_busqueda, 700, 500)
    ventana_busqueda.title("Busqueda de Productos")
    ventana_busqueda.geometry("700x500")

    tabla = ttk.Treeview(
        ventana_busqueda,
        columns=("nombre", "precio_venta","departamento"),
        show="headings"
    )

# ---ENCABEZADOS---

    tabla.heading("nombre", text="Descripcion del producto", anchor="w")
    tabla.heading("precio_venta", text="Precio venta", anchor="e")
    tabla.heading("departamento", text="Departamento", anchor="w")

# ---Ancho de columnas---

    tabla.column("nombre", width=450, anchor="w", stretch=False)
    tabla.column("precio_venta", width=100, anchor="e", stretch=False)
    tabla.column("departamento", width=100, anchor="w", stretch=False)
   
    entrada = tk.Entry(
        ventana_busqueda,
        font=("Arial", 20),
        width=40
    )

    entrada.pack(pady=10)
    tabla.pack(fill="both", expand=True)
 
    def buscar(event=None):

        texto = entrada.get()
    
        tabla.delete(*tabla.get_children())

        resultados = caja.buscar_productos_nombre(entrada.get())
        for producto in resultados:
        
            tabla.insert(
                     "",
                     tk.END,
                     iid=producto["codigo_barras"],
                     values=(
                         producto["nombre"],
                         f"${float(producto['precio_venta']):.2f}",
                         producto["departamento"]
                     )
                )
        items = tabla.get_children()

        if items:
            tabla.focus(items[0])
            tabla.selection_set(items[0])
    
    def bajar_a_tabla(event=None):
        items = tabla.get_children()

        if len(items) > 1:
            tabla.focus(items[1])
            tabla.selection_set(items[1])
        elif items:
            tabla.focus(items[0])
            tabla.selection_set(items[0])
       
        tabla.focus_set()

        return "break"

    def mover_abajo_busqueda(event=None):
        item = tabla.focus()

        if not item:
            return "break"

        siguiente = tabla.next(item)

        if siguiente:
            tabla.focus(siguiente)
            tabla.selection_set(siguiente)

        return "break"

    def mover_arriba_busqueda(event=None):

        item = tabla.focus()

        if not item:
            return "break"

        anterior = tabla.prev(item)

        if anterior:
            tabla.focus(anterior)
            tabla.selection_set(anterior)

        return "break"

    def seleccionar_primer_item(event=None):
    
        items = tabla.get_children()

        if not items:
            return
    
        tabla.selection_set(items[0])
        tabla.focus(items[0])

        seleccionar()

    def seleccionar(event=None):
        
        item = tabla.focus()

        if not item:
            return

        codigo = item

        caja.agregar_al_carrito(codigo)
        actualizar_tabla(codigo)

        ventana_busqueda.destroy()
        
        entrada_codigo_venta.focus_set()
    
    def cerrar_busqueda(event=None):
        ventana_busqueda.destroy()
        entrada_codigo_venta.focus_set()
        return "break"

    # ---- BINDS DE BUSQUEDA -----
    entrada.bind("<KeyRelease>", buscar)
    entrada.bind("<Down>", bajar_a_tabla)
    entrada.bind("<Return>", seleccionar_primer_item)

    ventana_busqueda.bind("<Escape>", cerrar_busqueda)

    tabla.bind("<Down>", mover_abajo_busqueda)
    tabla.bind("<Up>", mover_arriba_busqueda)
    tabla.bind("<Return>", seleccionar)
    tabla.bind("<Double-Button-1>", seleccionar)
    ventana_busqueda.after(100, lambda: entrada.focus_force())

    return "break"

def mover_abajo(event=None):

    global codigo_seleccionado

    items = tabla_venta.get_children()

    if not items:
        return "break"

    codigos = []

    for item in items:
        codigos.append(tabla_venta.item(item, "values")[0])

    if codigo_seleccionado not in codigos:
        codigo_seleccionado = codigos[0]
    else:
        indice = codigos.index(codigo_seleccionado)

        if indice < len(codigos) - 1:
            codigo_seleccionado = codigos[indice + 1]

    seleccionar_producto(codigo_seleccionado)

    return "break"

def mover_arriba(event=None):

    global codigo_seleccionado

    items = tabla_venta.get_children()

    if not items:
        return "break"

    codigos = [tabla_venta.item(item, "values")[0] for item in items]

    if codigo_seleccionado not in codigos:
        codigo_seleccionado = codigos[0]
    else:
        indice = codigos.index(codigo_seleccionado)

        if indice > 0:
            codigo_seleccionado = codigos[indice - 1]

    seleccionar_producto(codigo_seleccionado)

    return "break"
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

# --- Titulo (Venta de productos)---

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
btn_enter.pack(side="left", padx=5)

entrada_codigo_venta.bind("<Return>", agregar_al_carrito)
entrada_codigo_venta.bind("+", aumentar_cantidad)
entrada_codigo_venta.bind("-", disminuir_cantidad)
entrada_codigo_venta.bind("<Delete>", eliminar_producto)

frame_codigo_venta.columnconfigure(0, weight=1)

# --- Botones para venta ---

frame_botones_ventas = tk.Frame(frame_ventas)
frame_botones_ventas.grid(row=2, column=0, sticky="w", pady=(2,2))

btn_venta_rapida = tk.Button(frame_botones_ventas, text="CTRL+P VR",)
btn_venta_rapida.pack(side="left", padx=5)

btn_buscar = tk.Button(frame_botones_ventas, text="F10: Buscar", command=abrir_busqueda)
btn_buscar.pack(side="left", padx=5)

btn_entradas = tk.Button(frame_botones_ventas, text="F4 Entradas")
btn_entradas.pack(side="left", padx=5)

btn_salidas = tk.Button(frame_botones_ventas, text="F5 Salidas")
btn_salidas.pack(side="left", padx=5)

btn_borrar_articulo = tk.Button(frame_botones_ventas, text="Borrar Articulo", command=eliminar_producto)
btn_borrar_articulo.pack(side="left", padx=5)

# !--- Tabla carrito en F1 ---!

tabla_venta = ttk.Treeview(
    frame_ventas,
    columns =(
        "codigo",
        "descripcion",
        "precio",
        "cantidad",
        "importe",
        "existencias"
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
tabla_venta.heading("existencias", text="Existencias")

# !---Ancho de columnas---!

tabla_venta.column("codigo", width=100, anchor="center", stretch=False)
tabla_venta.column("descripcion", width=220, anchor="w", stretch=False)
tabla_venta.column("precio", width=100, anchor="center", stretch=False)
tabla_venta.column("cantidad", width=60, anchor="center", stretch=False)
tabla_venta.column("importe", width=80, anchor="center", stretch=False)
tabla_venta.column("existencias", width=60, anchor="center", stretch=False)

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

btn_ventas = tk.Button(barra_funciones, text="F1:Ventas", command=mostrar_ventas)
btn_ventas.pack(side="left", padx=10, pady=2)

btn_productos = tk.Button(
    barra_funciones,
    text="F2 : Productos",
    command=mostrar_productos
)
btn_productos.pack(side="left", padx=10, pady=2)

#-----------------F2 Productos-----------------

frame_productos = tk.Frame(ventana)

# ! --- Titulo (Productos) --- !

tk.Label(frame_productos, text="Nuevo producto", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=2)

# ! --- Botones para productos --- !

frame_botones_productos = tk.Frame(frame_productos)
frame_botones_productos.grid(row=1, column=0, columnspan=2, sticky="w", pady=5)

tk.Button(frame_botones_productos, text="Nuevo").pack(side="left", padx=5)
tk.Button(frame_botones_productos, text="Modificar").pack(side="left", padx=5)
tk.Button(frame_botones_productos, text="Eliminar").pack(side="left", padx=5)

# formulario 

frame_formulario = tk.Frame(frame_productos)
frame_formulario.grid(row=2, column=0, sticky="nw")

frame_formulario.columnconfigure(0, minsize=120)
frame_formulario.columnconfigure(1, minsize=350)

tk.Label(frame_formulario, text= "Codigo de barras").grid(row=0, column=0, sticky="e", padx=2)
entrada_codigo = tk.Entry(frame_formulario, width=40)
entrada_codigo.grid(row=0, column=1, sticky="w", padx=2)

tk.Label(frame_formulario, text="Descripción").grid(row=1, column=0, sticky="e", padx=2)
entrada_nombre = tk.Entry(frame_formulario, width=60)
entrada_nombre.grid(row=1, column=1, sticky="w", padx=2)

tk.Label(frame_formulario, text="Se vende").grid(row=2, column=0, sticky="e", padx=2)

frame_tipo_venta = tk.Frame(frame_formulario)
frame_tipo_venta.grid(row=2, column=1, sticky="w", pady=2)

tipo_venta = tk.StringVar(value="unidad")

radio_unidad = tk.Radiobutton(frame_tipo_venta, text="Por unidad/pza", variable=tipo_venta, value="unidad").grid(row=0, column=0, padx=2, sticky="w")
radio_granel = tk.Radiobutton(frame_tipo_venta, text="A granel(usa decimales)", variable=tipo_venta, value="granel").grid(row=0, column=1, padx=2, sticky="w")
radio_kit = tk.Radiobutton(frame_tipo_venta, text="Como paquete(Kit)", variable=tipo_venta, value="kit").grid(row=0, column=2, padx=2, sticky="w")

tk.Label(frame_formulario, text="Precio costo").grid(row=3, column=0, sticky="e", padx=2)
entrada_costo = tk.Entry(frame_formulario, width=12)
entrada_costo.grid(row=3, column=1, sticky="w", padx=2)

tk.Label(frame_formulario, text="Precio venta").grid(row=4, column=0, sticky="e", padx=2)
entrada_precio = tk.Entry(frame_formulario, width=12)
entrada_precio.grid(row=4, column=1, sticky="w", padx=2)

tk.Label(frame_formulario, text="Precio mayoreo").grid(row=5, column=0, sticky="e", padx=2)
entrada_mayoreo = tk.Entry(frame_formulario, width=12)
entrada_mayoreo.grid(row=5, column=1, sticky="w", padx=2)

tk.Label(frame_formulario, text="Departamento").grid(row=6, column=0, sticky="e", padx=2)

combo_departamento = ttk.Combobox(frame_formulario, values=["Abarrotes","Bimbo","Lala", "Coca cola"])
combo_departamento.set("Abarrotes")
combo_departamento.grid(row=6, column=1, sticky="w", padx=2)

control_inventario = tk.BooleanVar(value=True)
tk.Label(frame_formulario, text="Inventario").grid(row=7, column=0, sticky="e", padx=2)

check_inventario = tk.Checkbutton(frame_formulario, text="Este producto utiliza inventario", variable=control_inventario)
check_inventario.grid(row=7, column=1, sticky="w", padx=2)

tk.Label(frame_formulario, text="Cantidad actual").grid(row=8, column=0, sticky="e", padx=5)
entrada_cantidad_actual = tk.Entry(frame_formulario, width=12)
entrada_cantidad_actual.grid(row=8, column=1, sticky="w", padx=2)

tk.Label(frame_formulario, text="Minimo").grid(row=9, column=0, sticky="e", padx=2)
entrada_minimo = tk.Entry(frame_formulario, width=12)
entrada_minimo.grid(row=9, column=1, sticky="w", padx=2)

tk.Button(frame_formulario, text= "Agregar producto", width=40, command=agregar_producto).grid(row=10, column=0, columnspan=2, padx=5, pady=5)

#teclas

ventana.bind("<F1>", mostrar_ventas)
ventana.bind("<F2>", mostrar_productos)
ventana.bind("<F10>", abrir_busqueda)
ventana.bind("<Up>", mover_arriba)
ventana.bind("<Down>", mover_abajo)

entrada_codigo_venta.focus_set()

#Mainloop
ventana.mainloop()