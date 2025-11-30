import datetime

class FacturaComision:
    def __init__(
        self,
        id=None,
        id_transaccion=None,

        numero_factura=None,
        fecha: datetime.datetime = None,

        # vendedor (snapshot)
        id_vendedor=None,
        nombre_vendedor=None,
        nombre_negocio=None,
        direccion_vendedor=None,
        es_contribuyente=None,
        porcentaje_iva=None,

        # producto (snapshot)
        nombre_producto=None,
        unidades_vendidas=None,
        precio_unitario=None,
        precio_total_venta=None,

        # comisión
        porcentaje_comision=None,
        monto_comision=None,
        monto_iva_comision=None,
        total_a_pagar=None,

        # información adicional
        estado_pago=None,
        metodo_pago=None
    ):

        self.id: int = id
        self.id_transaccion: int = id_transaccion

        self.numero_factura: str = numero_factura
        self.fecha: datetime.datetime = fecha

        # vendedor snapshot
        self.id_vendedor: int = id_vendedor
        self.nombre_vendedor: str = nombre_vendedor
        self.nombre_negocio: str = nombre_negocio
        self.direccion_vendedor: str = direccion_vendedor
        self.es_contribuyente: bool = es_contribuyente
        self.porcentaje_iva: float = porcentaje_iva

        # producto snapshot
        self.nombre_producto: str = nombre_producto
        self.unidades_vendidas: int = unidades_vendidas
        self.precio_unitario: float = precio_unitario
        self.precio_total_venta: float = precio_total_venta

        # comisión
        self.porcentaje_comision: float = porcentaje_comision
        self.monto_comision: float = monto_comision
        self.monto_iva_comision: float = monto_iva_comision
        self.total_a_pagar: float = total_a_pagar

        # información adicional
        self.estado_pago: str = estado_pago
        self.metodo_pago: str = metodo_pago