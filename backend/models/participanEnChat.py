class ParticipanEnChat:
    def __init__(
        self,
        id_usuario=None,
        id_chat=None,
        rol_en_chat=None
    ):

        self.id_usuario: int = id_usuario
        self.id_chat: int = id_chat
        self.rol_en_chat: str = rol_en_chat