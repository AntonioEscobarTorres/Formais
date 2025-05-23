class Estado:
    def __init__(self, estado_inicial: str):
        # Divide o estado por 'q' e remonta nomes reais de estados
        estados_raw = estado_inicial.strip().split('q')
        self.estados_menores = sorted(
            {'q' + e for e in estados_raw if e != ''}
        )
        self.estado = ''.join(self.estados_menores)

    def get_estado(self):
        return self.estado

    def __str__(self):
        return "{" + self.estado + "}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, Estado) and self.estado == other.estado

    def __hash__(self):
        return hash(self.estado)
