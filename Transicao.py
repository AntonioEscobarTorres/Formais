from Estado import Estado

class Transicao():

    def __init__(self,
                 origem: Estado, simbolo: str,
                 destino: Estado):


        self.origem = origem
        self.simbolo = simbolo
        self.destino = destino
