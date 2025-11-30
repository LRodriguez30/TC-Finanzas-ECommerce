import datetime
from decimal import Decimal

class Transaccion:
    def __init__(
        self,
        id=None,
        id_producto=None,
        id_comprador=None,
        id_vendedor=None,
        id_estado_transaccion=None,
        id_metodo_pago=None,
        precio_unitario=None,
        unidades_compradas=None,
        precio_envio=None,
        descuento=None,
        precio_total=None,
        costo_unitario=None,
        fecha=None
    ):
        self.id: int = id
        self.id_producto: int = id_producto
        self.id_comprador: int = id_comprador
        self.id_vendedor: int = id_vendedor
        self.id_estado_transaccion: int = id_estado_transaccion
        self.id_metodo_pago: int = id_metodo_pago
        self.precio_unitario: Decimal = precio_unitario
        self.unidades_compradas: int = unidades_compradas
        self.precio_envio: Decimal = precio_envio
        self.descuento: Decimal = descuento
        self.precio_total: Decimal = precio_total
        self.costo_unitario: Decimal = costo_unitario
        self.fecha: datetime = fecha