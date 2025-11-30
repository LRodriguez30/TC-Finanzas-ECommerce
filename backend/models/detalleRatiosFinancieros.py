class DetalleRatioFinanciero:
    def __init__(
        self,
        id=None,
        id_ratio=None,
        nombre_componente=None,  # Ej: "Inventarios", "CostoVentas"
        valor=0.0,
        id_cuenta=None
    ):

        self.id: int = id
        self.id_ratio: int = id_ratio
        self.nombre_componente: str = nombre_componente
        self.valor: float = valor
        self.id_cuenta: int = id_cuenta  # Puede ser None si no proviene de una cuenta específica