class imagenProducto:
    def __init__(
        self,
        id=None,
        id_producto=None,
        url_imagen=None
    ):
        self.id: int = id
        self.id_producto: int = id_producto
        self.url_imagen: str = url_imagen