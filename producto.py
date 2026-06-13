class ProductoInventario:

    def __init__(self, codigo_barras, nombre, tipo_venta, precio_costo, 
                 precio_venta, precio_mayoreo, departamento):

        self.codigo_barras = codigo_barras
        self.nombre = nombre
        self.tipo_venta = tipo_venta
        self.precio_costo = precio_costo
        self.precio_venta = precio_venta
        self.precio_mayoreo = precio_mayoreo
        self.departamento = departamento

    def to_dict(self):

        return {
            "codigo_barras": self.codigo_barras,
            "nombre": self.nombre,
            "tipo_venta": self.tipo_venta,
            "precio_costo": self.precio_costo,
            "precio_venta": self.precio_venta,
            "precio_mayoreo": self.precio_mayoreo,
            "departamento": self.departamento
        }

class ProductoCarrito:

    def __init__(self, codigo, nombre, precio, cantidad=1):

        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    def subtotal(self):
 
        return self.precio * self.cantidad

    def to_dict(self):

        return{
           "codigo" : self.codigo,
           "nombre" : self.nombre,
           "precio" : self.precio,
           "cantidad" : self.cantidad
              }