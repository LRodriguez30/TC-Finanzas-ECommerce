import datetime

class MovimientoContable:
    def __init__(
        self,
        id=None,
        id_comprobante=None,
        id_periodo=None,
        id_cuenta=None,
        id_transaccion=None,
        id_factura=None,
        id_vendedor=None,
        es_movimiento_plataforma=False,
        fecha: datetime = None,
        debe=0.0,
        haber=0.0,
        descripcion=None
    ):

        self.id: int = id
        self.id_comprobante: int = id_comprobante
        self.id_periodo: int = id_periodo
        self.id_cuenta: int = id_cuenta
        self.id_transaccion: int = id_transaccion
        self.id_factura: int = id_factura
        self.id_vendedor: int = id_vendedor
        self.es_movimiento_plataforma: bool = es_movimiento_plataforma

        self.fecha: datetime = fecha or datetime.datetime.now()

        # Valores contables
        self.debe: float = debe
        self.haber: float = haber
        self.descripcion: str = descripcion

        # Validaciones opcionales
        if (self.debe > 0 and self.haber > 0) or (self.debe == 0 and self.haber == 0):
            raise ValueError("Solo uno de Debe o Haber debe ser mayor a 0")

        if (self.id_vendedor is not None and self.es_movimiento_plataforma) or \
            (self.id_vendedor is None and not self.es_movimiento_plataforma):
            raise ValueError("El movimiento debe pertenecer a un vendedor o a la plataforma, no ambos")