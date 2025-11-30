class Vendedor:    
    def __init__(
        self,
        id=None,
        id_usuario=None,
        nombre_negocio=None,
        logo_negocio=None,
        descripcion_negocio=None,
        EsContribuyente=None
    ):
        self.id_vendedor = id
        self.id_usuario = id_usuario
        self.nombre_negocio = nombre_negocio
        self.logo_negocio = logo_negocio
        self.descripcion_negocio = descripcion_negocio
        self.EsContribuyente = EsContribuyente