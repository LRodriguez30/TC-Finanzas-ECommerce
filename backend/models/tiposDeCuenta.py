class TipoCuenta:
    def __init__(
        self,
        id=None,
        nombre=None,
        categoria=None,
        descripcion=None
    ):

        self.id: int = id
        self.nombre: str = nombre        # Ej: Activo, Pasivo, Capital, Ingreso, Gasto
        self.categoria: str = categoria  # Ej: Corriente, No corriente, Operativo, etc.
        self.descripcion: str = descripcion
