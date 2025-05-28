class Estado:
    def __init__(self, estado_str: str):
        self.estado = estado_str.strip()

    def get_estado(self) -> str:
        return self.estado

    def __str__(self):
        return self.estado

    def __repr__(self):
        return f"Estado('{self.estado}')"

    def __eq__(self, other):
        if isinstance(other, Estado):
            return self.estado == other.estado
        return False

    def __hash__(self):
        return hash(self.estado)