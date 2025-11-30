import datetime
import uuid

class RefreshToken:
    def __init__(
        self,
        id=None,
        id_usuario=None,
        token: uuid.UUID = None,
        fecha_creacion: datetime.datetime = None,
        fecha_expiracion: datetime.datetime = None,
        revoked: bool = None
    ):

        self.id: int = id
        self.id_usuario: int = id_usuario

        # Token UNIQUEIDENTIFIER → usar uuid.UUID
        self.token: uuid.UUID = token or uuid.uuid4()
        self.fecha_creacion: datetime.datetime = fecha_creacion or datetime.datetime.now()
        self.fecha_expiracion: datetime.datetime = fecha_expiracion
        self.revoked: bool = revoked if revoked is not None else False