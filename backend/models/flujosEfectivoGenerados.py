import datetime

class FlujoEfectivoGenerado:
    def __init__(
        self,
        id=None,
        id_periodo=None,
        id_vendedor=None,
        es_flujo_plataforma=False,
        flujo_operacion=0.0,
        flujo_inversion=0.0,
        flujo_financiamiento=0.0,
        aumento_disminucion_efectivo=0.0,
        efectivo_inicial=0.0,
        efectivo_final=0.0,
        metodo=None,  # "Directo" o "Indirecto"
        fecha_generacion: datetime.datetime = None
    ):

        self.id: int = id
        self.id_periodo: int = id_periodo
        self.id_vendedor: int = id_vendedor
        self.es_flujo_plataforma: bool = es_flujo_plataforma

        # Flujo de efectivo por actividades
        self.flujo_operacion: float = flujo_operacion
        self.flujo_inversion: float = flujo_inversion
        self.flujo_financiamiento: float = flujo_financiamiento

        # Totales
        self.aumento_disminucion_efectivo: float = aumento_disminucion_efectivo
        self.efectivo_inicial: float = efectivo_inicial
        self.efectivo_final: float = efectivo_final

        self.metodo: str = metodo  # "Directo" o "Indirecto"

        self.fecha_generacion: datetime.datetime = fecha_generacion or datetime.datetime.now()