from Analisador_Lexico.Estado import Estado

    # Representa uma transição entre dois estados em um autômato,
    # Ativada por um símbolo específico.
class Transicao:

    # Inicializa uma transição com estado de 
    # origem, símbolo de transição e estado de destino.
    def __init__(self, origem: Estado, simbolo: str, destino: Estado):
        self.origem = origem
        self.simbolo = simbolo
        self.destino = destino

    # Retorna o símbolo da transição
    def get_simbolo(self) -> str:
        return self.simbolo
    # Retorna o estado de origem da transição
    def get_origem(self) -> Estado:
        return self.origem
    # Retorna o estado destino da transição
    def get_destino(self) -> Estado:
        return self.destino

    # Retorna uma representação legível da transição, com o símbolo em amarelo.
    # Útil para impressão no terminal.
    def __str__(self):
        return f"{self.origem.get_estado()},{self.simbolo},{self.destino.get_estado()}"

