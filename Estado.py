# Representa um estado de um autômato, identificado por uma string.

class Estado:
    def __init__(self, estado_str: str):
        self.estado = estado_str.strip()

    # Retorna o nome do estado 
    def get_estado(self) -> str:
        return self.estado

    # Usado pra impressão
    def __str__(self):
        return self.estado

