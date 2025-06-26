class Simbolo:
    
    def __init__(self, nome, tipo):
        self.nome = nome
        # Terminal ou não terminal
        self.tipo = tipo

    def  obter_nome(self):
        return self.nome
    
    def obter_tipo(self):
        return self.tipo
    
    def __str__(self):
        return f"Simbolo({self.nome}, do tipo {self.tipo})"