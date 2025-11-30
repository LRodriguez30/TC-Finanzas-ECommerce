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
        self.id_usuario = id
        self.id_rol = id_rol
        self.primer_nombre = primer_nombre
        self.segundo_nombre = segundo_nombre
        self.primer_apellido = primer_apellido
        self.segundo_apellido = segundo_apellido
        self.telefono = telefono
        self.correo = correo
        self.contraseña = contraseña
        self.fecha_registro = fecha_registro