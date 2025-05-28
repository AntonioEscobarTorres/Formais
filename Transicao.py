from Estado import Estado

class Transicao:
    def __init__(self, origem: Estado, simbolo: str, destino: Estado):
        self.origem = origem
        self.simbolo = simbolo
        self.destino = destino

    def get_simbolo(self) -> str:
        return self.simbolo

    def get_origem(self) -> Estado:
        return self.origem

    def get_destino(self) -> Estado:
        return self.destino

    def __str__(self):
        AMARELO = '\033[93m'
        RESET = '\033[0m'
        return f"{self.origem.get_estado()},{AMARELO}{self.simbolo}{RESET},{self.destino.get_estado()}"

    def __repr__(self):
        return f"Transicao(Estado('{self.origem.get_estado()}'), '{self.simbolo}', Estado('{self.destino.get_estado()}'))"

    def __eq__(self, other):
        if isinstance(other, Transicao):
            return self.origem == other.origem and \
                   self.simbolo == other.simbolo and \
                   self.destino == other.destino
        return False

    def __hash__(self):
        return hash((self.origem, self.simbolo, self.destino))
