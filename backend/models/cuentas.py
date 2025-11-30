class Cuenta:
    def __init__(
        self,
        id=None,
        id_tipo_cuenta=None,
        id_vendedor=None,
        es_cuenta_plataforma=False,
        nombre_cuenta=None,
        codigo_cuenta=None,
        es_afectable=True,
        es_cuenta_de_sistema=False,
        descripcion=None,
        saldo_actual=0.0
    ):

        self.id: int = id
        self.id_tipo_cuenta: int = id_tipo_cuenta

        # Dueño de la cuenta
        self.id_vendedor: int = id_vendedor
        self.es_cuenta_plataforma: bool = es_cuenta_plataforma

        # Identificación de la cuenta
        self.nombre_cuenta: str = nombre_cuenta
        self.codigo_cuenta: str = codigo_cuenta

        # Propiedades contables
        self.es_afectable: bool = es_afectable
        self.es_cuenta_de_sistema: bool = es_cuenta_de_sistema

        self.descripcion: str = descripcion
        self.saldo_actual: float = saldo_actual