class Vendedor:    
    def __init__(
        self,
        id=None,
        id_usuario=None,
        nombre_negocio=None,
        logo_negocio=None,
        descripcion_negocio=None,
        es_contribuyente=None
    ):
        self.id: int = id
        self.id_usuario: int = id_usuario
        self.nombre_negocio: str = nombre_negocio
        self.logo_negocio: str = logo_negocio
        self.descripcion_negocio: str = descripcion_negocio
        self.es_contribuyente: bool = es_contribuyente