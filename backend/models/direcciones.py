class Direccion:
    def __init__(
        self,
        id=None,
        id_vendedor=None,
        id_comprador=None,

        calle=None,
        barrio=None,
        ciudad=None,
        departamento=None,
        codigo_postal=None,
        alias_direccion=None,
        ubicacion=None,
        es_principal=None
    ):

        self.id: int = id
        self.id_vendedor: int = id_vendedor
        self.id_comprador: int = id_comprador

        self.calle: str = calle
        self.barrio: str = barrio
        self.ciudad: str = ciudad
        self.departamento: str = departamento
        self.codigo_postal: str = codigo_postal
        self.alias_direccion: str = alias_direccion

        # Ubicación geográfica (GEOGRAPHY en SQL, se puede manejar como texto, dict o WKT)
        self.ubicacion: dict = ubicacion                    #diccionario de ejemplo para ubicaciones  self.ubicacion = {
                                                            #"lat": None,
                                                            #"lng": None
                                                            #}
        # EsPrincipal BIT
        self.es_principal: bool = es_principal