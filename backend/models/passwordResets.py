import datetime

class PasswordReset:
    def __init__(
        self,
        id=None,
        id_usuario=None,
        token=None,
        expira: datetime = None,
        usado: bool = None
    ):

        self.id: int = id
        self.id_usuario: int = id_usuario

        self.token: str = token  # UNIQUEIDENTIFIER en SQL Server → string en Python
        self.expira: datetime = expira
        self.usado: bool = usado