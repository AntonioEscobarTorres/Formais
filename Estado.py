class Estado:



    def __init__(self, estado_inicial: str):
        self.estados_menores = []
        self.estado = ''.join(sorted(estado_inicial.strip()))
        

        for a in self.estado:
            self.estados_menores.append(a)

    def get_estado(self):
        return self.estado

    def __str__(self):
        return "{" + self.get_estado() + "}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, Estado) and self.estado == other.estado

    def __hash__(self):
        return hash(self.estado)

