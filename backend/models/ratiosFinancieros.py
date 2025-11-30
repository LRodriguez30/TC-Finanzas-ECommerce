import datetime

class RatioFinanciero:
    def __init__(
        self,
        id=None,
        id_periodo=None,
        id_vendedor=None,
        es_ratio_plataforma=False,
        # Razones de liquidez
        razon_corriente=None,
        prueba_acida=None,
        # Razones de actividad
        rotacion_inventarios=None,
        rotacion_cuentas_por_cobrar=None,
        periodo_promedio_cobro=None,
        rotacion_activos_fijos=None,
        rotacion_activos_totales=None,
        # Razones de endeudamiento
        deuda_total_sobre_activos=None,
        deuda_capital=None,
        rotacion_intereses_a_utilidades=None,
        # Razones de rentabilidad
        margen_bruto=None,
        margen_operativo=None,
        margen_neto=None,
        roa=None,
        roe=None,
        # Sistema DuPont
        dupont_margen_neto=None,
        dupont_rotacion_activos=None,
        dupont_apalancamiento_financiero=None,
        dupont_roe=None,
        fecha_generacion: datetime.datetime = None
    ):

        self.id: int = id
        self.id_periodo: int = id_periodo
        self.id_vendedor: int = id_vendedor
        self.es_ratio_plataforma: bool = es_ratio_plataforma

        # Liquidez
        self.razon_corriente: float = razon_corriente
        self.prueba_acida: float = prueba_acida

        # Actividad
        self.rotacion_inventarios: float = rotacion_inventarios
        self.rotacion_cuentas_por_cobrar: float = rotacion_cuentas_por_cobrar
        self.periodo_promedio_cobro: float = periodo_promedio_cobro
        self.rotacion_activos_fijos: float = rotacion_activos_fijos
        self.rotacion_activos_totales: float = rotacion_activos_totales

        # Endeudamiento
        self.deuda_total_sobre_activos: float = deuda_total_sobre_activos
        self.deuda_capital: float = deuda_capital
        self.rotacion_intereses_a_utilidades: float = rotacion_intereses_a_utilidades

        # Rentabilidad
        self.margen_bruto: float = margen_bruto
        self.margen_operativo: float = margen_operativo
        self.margen_neto: float = margen_neto
        self.roa: float = roa
        self.roe: float = roe

        # Sistema DuPont
        self.dupont_margen_neto: float = dupont_margen_neto
        self.dupont_rotacion_activos: float = dupont_rotacion_activos
        self.dupont_apalancamiento_financiero: float = dupont_apalancamiento_financiero
        self.dupont_roe: float = dupont_roe

        self.fecha_generacion: datetime.datetime = fecha_generacion or datetime.datetime.now()

        # Validación de dueño
        if (self.id_vendedor is not None and self.es_ratio_plataforma) or \
            (self.id_vendedor is None and not self.es_ratio_plataforma):
            raise ValueError("El ratio financiero debe pertenecer a un vendedor o a la plataforma, no ambos")