import datetime

class Mensaje:
    def __init__(
        self,
        id=None,
        id_chat=None,
        id_usuario=None,
        contenido=None,
        fecha_envio: datetime.datetime = None,
        estado_mensaje=None
    ):

        self.id: int = id
        self.id_chat: int = id_chat
        self.id_usuario: int = id_usuario

        self.contenido: str = contenido
        self.fecha_envio: datetime.datetime = fecha_envio
        self.estado_mensaje: str = estado_mensaje
