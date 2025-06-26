from Analisador_Sintatico.Simbolo import Simbolo

class Producao:
    def __init__(self, cabeca, corpo : Simbolo):
        self.cabeca = cabeca
        self.corpo = corpo

    def obter_cabeca(self):
        return self.cabeca
    
    def obter_corpo(self):
        return self.corpo
    
    def __str__(self):
        #return f"{self.cabeca} -> {self.corpo.obter_nome()}"
        # Itera sobre cada objeto Simbolo no corpo e obtém o seu nome.
        corpo_str = ' '.join([s.obter_nome() for s in self.corpo])
        
        # Trata o caso de produção vazia (epsilon).
        if not corpo_str:
            corpo_str = '&'
            
        return f"{self.cabeca} -> {corpo_str}"

    def __eq__(self, other):
        if not isinstance(other, Producao):
            return NotImplemented
        # Compara a cabeça e a representação em string do corpo.
        return self.obter_cabeca() == other.obter_cabeca() and \
               str(self.obter_corpo()) == str(other.obter_corpo())

    def __hash__(self):
        # Cria um hash baseado na cabeça e nos nomes dos símbolos do corpo.
        corpo_nomes = tuple(s.obter_nome() for s in self.corpo)
        return hash((self.cabeca, corpo_nomes))