class Venta:

    def __init__(self, folio, fecha, productos, total):

        self.folio = folio
        self.fecha = fecha
        self.productos = productos
        self.total = total

    def to_dict(self):
        
        return {
                 "folio" : self.folio,
                 "fecha" : self.fecha,
                 "total" : self.total,
                 "productos" : [producto.to_dict() for producto in self.productos]
               }