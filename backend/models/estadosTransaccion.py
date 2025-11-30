class EstadosTransaccion:
    def __init__(
        self,
        id=None,
        nombre_estado_transaccion=None
    ):
        self.id: int = id
        self.nombre_estado_transaccion: str = nombre_estado_transaccion