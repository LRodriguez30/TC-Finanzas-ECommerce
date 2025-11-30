import datetime

class ReseñaProducto:
    def __init__(
        self,
        id=None,
        id_producto=None,
        id_comprador=None,
        id_transaccion=None,
        calificacion=None,
        comentario=None,
        fecha_reseña: datetime = None
    ):

        self.id: int = id
        self.id_producto: int = id_producto
        self.id_comprador: int = id_comprador
        self.id_transaccion: int = id_transaccion

        self.calificacion: float = calificacion
        self.comentario: str = comentario
        self.fecha_reseña: datetime = fecha_reseña