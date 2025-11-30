class EstadoProducto:
    def __init__(
        self,
        id=None,
        nombre_estado=None
    ):
        self.id: int = id
        self.nombre_estado: str = nombre_estado