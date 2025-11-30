import datetime

class ComisionPorTransaccion:
    def __init__(
        self,
        id=None,
        id_transaccion=None,
        id_vendedor=None,
        porcentaje=None,
        monto_comision=None,
        fecha=None
    ):
        self.id: int = id
        self.id_transaccion: int = id_transaccion
        self.id_vendedor: int = id_vendedor
        self.porcentaje: float = porcentaje
        self.monto_comision: float = monto_comision
        self.fecha: datetime = fecha

