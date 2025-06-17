from src.Simbolo import Simbolo

class Producao:
    def __init__(self, cabeca, corpo : Simbolo):
        self.cabeca = cabeca
        self.corpo = corpo
        pass

    def obter_cabeca(self):
        return self.cabeca
    
    def obter_corpo(self):
        return self.corpo
    
    def __str__(self):

        return f"{self.cabeca} -> {self.corpo.obter_nome()}"