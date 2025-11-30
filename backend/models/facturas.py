import datetime

class Factura:
    def __init__(
        self,
        id=None,
        id_transaccion=None,

        numero_factura=None,
        fecha: datetime.datetime = None,

        # snapshot comprador
        nombre_comprador=None,
        correo_comprador=None,
        direccion_comprador=None,

        # snapshot vendedor
        nombre_vendedor=None,
        nombre_negocio=None,
        direccion_vendedor=None,
        es_contribuyente=None,
        porcentaje_iva=None,

        # snapshot producto
        nombre_producto=None,
        descripcion_producto=None,

        # valores económicos
        precio_unitario=None,
        unidades_compradas=None,
        descuento=None,
        precio_envio=None,

        subtotal_sin_iva=None,
        monto_iva=None,
        total=None,

        metodo_pago=None,
        estado_transaccion=None
    ):

        self.id: int = id
        self.id_transaccion: int = id_transaccion

        self.numero_factura: str = numero_factura
        self.fecha: datetime = fecha

        # snapshot comprador
        self.nombre_comprador: str = nombre_comprador
        self.correo_comprador: str = correo_comprador
        self.direccion_comprador: str = direccion_comprador

        # snapshot vendedor
        self.nombre_vendedor: str = nombre_vendedor
        self.nombre_negocio: str = nombre_negocio
        self.direccion_vendedor: str = direccion_vendedor
        self.es_contribuyente: bool = es_contribuyente
        self.porcentaje_iva: float = porcentaje_iva

        # snapshot producto
        self.nombre_producto: str = nombre_producto
        self.descripcion_producto: str = descripcion_producto

        # valores económicos
        self.precio_unitario: float = precio_unitario
        self.unidades_compradas: int = unidades_compradas
        self.descuento: float = descuento
        self.precio_envio: float = precio_envio

        self.subtotal_sin_iva: float = subtotal_sin_iva
        self.monto_iva: float = monto_iva
        self.total: float = total

        self.metodo_pago: str = metodo_pago
        self.estado_transaccion: str = estado_transaccion