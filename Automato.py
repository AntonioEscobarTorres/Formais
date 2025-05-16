from Estado import Estado
from Transicao import Transicao

class Automato:

    def __init__(self, n_estados: int, inicial : Estado, finais : {Estado},
                 transicoes : {Transicao} ,alfabeto : {str}):
        
        self.n_estados = n_estados
        self.incial = inicial
        self.finais = finais
        self.transicoes = transicoes
        self.alfabeto = alfabeto

        