import datetime

class ReseñaVendedor:
    def __init__(
        self,
        id=None,
        id_vendedor=None,
        id_comprador=None,
        id_transaccion=None,
        calificacion=None,
        comentario=None,
        fecha_reseña: datetime = None
    ):

        self.id: int = id
        self.id_vendedor: int = id_vendedor
        self.id_comprador: int = id_comprador
        self.id_transaccion: int = id_transaccion

        self.calificacion: float = calificacion
        self.comentario: str = comentario
        self.fecha_reseña: datetime = fecha_reseña