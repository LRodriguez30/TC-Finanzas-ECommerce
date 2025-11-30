import datetime

class PeriodoContable:
    def __init__(
        self,
        id=None,
        fecha_inicio: datetime.date = None,
        fecha_fin: datetime.date = None,
        esta_cerrado: bool = False
    ):

        self.id: int = id
        self.fecha_inicio: datetime.date = fecha_inicio
        self.fecha_fin: datetime.date = fecha_fin
        self.esta_cerrado: bool = esta_cerrado

        # Validación opcional de rango
        if self.fecha_inicio and self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValueError("FechaFin no puede ser menor que FechaInicio")