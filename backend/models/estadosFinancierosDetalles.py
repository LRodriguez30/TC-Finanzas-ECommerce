class EstadoFinancieroDetalle:
    def __init__(
        self,
        id=None,
        id_estado=None,
        id_cuenta=None,
        tipo_estado=None,        # "Balance" o "Resultado"
        saldo=0.0,
        porcentaje_vertical=None,
        variacion_absoluta=None,
        variacion_porcentual=None
    ):

        self.id: int = id
        self.id_estado: int = id_estado
        self.id_cuenta: int = id_cuenta

        self.tipo_estado: str = tipo_estado
        self.saldo: float = saldo

        # Análisis contable opcional
        self.porcentaje_vertical: float = porcentaje_vertical
        self.variacion_absoluta: float = variacion_absoluta
        self.variacion_porcentual: float = variacion_porcentual