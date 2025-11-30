import datetime

class Chat:
    def __init__(
        self,
        id=None,
        id_producto=None,
        id_transaccion=None,
        fecha_inicio: datetime.datetime = None,
        fecha_final: datetime.datetime = None,
        estado: bool = None
    ):

        self.id: int = id
        self.id_producto: int = id_producto
        self.id_transaccion: int = id_transaccion

        # fechas
        self.fecha_inicio: datetime.datetime = fecha_inicio
        self.fecha_final: datetime.datetime = fecha_final

        # estado
        self.estado: bool = estado