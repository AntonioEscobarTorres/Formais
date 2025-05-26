from Estado import Estado

class Transicao():

    def __init__(self,
                 origem: Estado, simbolo: str,
                 destino: Estado):


        self.origem = origem
        self.simbolo = simbolo
        self.destino = destino

    def get_simbolo(self):
        return self.simbolo

    def get_origem(self):
        return self.origem

    def get_destino(self):
        return self.destino




    def __str__(self):
        AMARELO = '\033[93m'
        RESET = '\033[0m'
        return f"{self.origem},{AMARELO}{self.simbolo}{RESET},{self.destino}"


    def __repr__(self):
        return self.__str__()