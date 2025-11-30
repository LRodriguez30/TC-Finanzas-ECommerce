class SaldoInicial:
    def __init__(
        self,
        id=None,
        id_cuenta=None,
        id_periodo=None,
        saldo_inicial=0.0
    ):

        self.id: int = id
        self.id_cuenta: int = id_cuenta
        self.id_periodo: int = id_periodo
        self.saldo_inicial: float = saldo_inicial
