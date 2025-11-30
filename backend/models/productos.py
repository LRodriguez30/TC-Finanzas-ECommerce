import datetime

class Producto:
    def __init__(
        self,
        id=None,
        id_vendedor=None,
        id_categoria=None,
        id_estado_producto=None,
        nombre_producto=None,
        precio=None,
        descripcion=None,
        stock_disponible=None,
        fecha_publicacion=None
    ):
        self.id_producto: int = id
        self.id_vendedor: int = id_vendedor
        self.id_categoria: int = id_categoria
        self.id_estado_producto: int = id_estado_producto
        self.nombre_producto: str = nombre_producto
        self.precio: float = precio
        self.descripcion: str = descripcion
        self.stock_disponible: int = stock_disponible
        self.fecha_publicacion: datetime = fecha_publicacion
