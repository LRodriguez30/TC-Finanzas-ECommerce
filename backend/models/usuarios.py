import datetime

class Usuario:
    def __init__(
        self,
        id=None,
        id_rol=None,
        primer_nombre=None,
        segundo_nombre=None,
        primer_apellido=None,
        segundo_apellido=None,
        telefono=None,
        correo=None,
        contraseña=None,
        fecha_registro=None
    ):
        self.id: int = id
        self.id_rol: int = id_rol
        self.primer_nombre: str = primer_nombre
        self.segundo_nombre: str = segundo_nombre
        self.primer_apellido: str = primer_apellido
        self.segundo_apellido: str= segundo_apellido
        self.telefono: str= telefono
        self.correo: str = correo
        self.contraseña: str = contraseña
        self.fecha_registro: datetime = fecha_registro