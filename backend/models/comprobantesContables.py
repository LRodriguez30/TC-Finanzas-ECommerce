import datetime

class ComprobanteContable:
    def __init__(
        self,
        id=None,
        fecha: datetime.datetime = None,
        tipo=None,
        descripcion=None,
        id_vendedor=None,
        es_comprobante_plataforma=False
    ):

        self.id: int = id
        self.fecha: datetime.datetime = fecha or datetime.datetime.now()
        self.tipo: str = tipo          # Ej: "Venta", "Compra", "Pago", "Ajuste"
        self.descripcion: str = descripcion

        # Vendedor o plataforma
        self.id_vendedor: int = id_vendedor
        self.es_comprobante_plataforma: bool = es_comprobante_plataforma