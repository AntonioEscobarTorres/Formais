class Estado:


    def __init__(self, estado_inicial: str):
        self.estados_menores = []
        self.estado = ''.join(sorted(estado_inicial.strip()))
        
        for a in self.estado:
            self.estados_menores.append(a)