import datetime

class EstadoFinancieroGenerado:
    def __init__(
        self,
        id=None,
        id_periodo=None,
        id_vendedor=None,
        es_estado_plataforma=False,
        total_activos=0.0,
        total_pasivos=0.0,
        total_capital=0.0,
        total_ingresos=0.0,
        total_gastos=0.0,
        utilidad_neta=0.0,
        fecha_generacion: datetime.datetime = None
    ):

        self.id: int = id
        self.id_periodo: int = id_periodo
        self.id_vendedor: int = id_vendedor
        self.es_estado_plataforma: bool = es_estado_plataforma

        # Totales contables
        self.total_activos: float = total_activos
        self.total_pasivos: float = total_pasivos
        self.total_capital: float = total_capital
        self.total_ingresos: float = total_ingresos
        self.total_gastos: float = total_gastos
        self.utilidad_neta: float = utilidad_neta

        # Fecha de generación
        self.fecha_generacion: datetime.datetime = fecha_generacion or datetime.datetime.now()

        # Validación de dueño
        if (self.id_vendedor is not None and self.es_estado_plataforma) or \
            (self.id_vendedor is None and not self.es_estado_plataforma):
            raise ValueError("El estado financiero debe pertenecer a un vendedor o a la plataforma, no ambos")