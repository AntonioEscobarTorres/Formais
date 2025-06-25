

from Analisador_Sintatico.TipoSimbolo import TipoSimbolo  

class ItemLR0:
    def __init__(self, producao, posicao_ponto):
        self.producao = producao
        self.posicao_ponto = posicao_ponto

    def obter_producao(self):
        return self.producao

    def obter_posicao_ponto(self):
        return self.posicao_ponto

    def obter_simbolo_apos_ponto(self):
        """Retorna o símbolo imediatamente após o ponto, ou None se o ponto estiver no final."""
        corpo = self.producao.obter_corpo()
        if self.posicao_ponto < len(corpo):
            # Ignora epsilon no corpo, pois não é um símbolo real de transição
            # Agora esta linha funcionará, pois TipoSimbolo está definido
            if corpo[self.posicao_ponto].obter_tipo() == TipoSimbolo.epsilon:
                return None
            return corpo[self.posicao_ponto]
        return None

    def esta_completo(self):
        """Verifica se o ponto está no final da produção."""
        corpo = self.producao.obter_corpo()
        # Se o corpo for epsilon, o item já está completo.
        if len(corpo) == 1 and corpo[0].obter_tipo() == TipoSimbolo.epsilon:
            return True
        return self.posicao_ponto == len(corpo)
    
    def avancar_ponto(self):
        """Retorna um novo item com o ponto avançado uma posição."""
        if not self.esta_completo():
            return ItemLR0(self.producao, self.posicao_ponto + 1)
        return self

    def __eq__(self, other):
        if not isinstance(other, ItemLR0):
            return NotImplemented
        
        # Compara a cabeça da produção.
        if self.producao.obter_cabeca() != other.producao.obter_cabeca():
            return False
            
        # Compara o corpo da produção, símbolo por símbolo.
        meu_corpo = self.producao.obter_corpo()
        outro_corpo = other.producao.obter_corpo()
        if len(meu_corpo) != len(outro_corpo):
            return False
        for s1, s2 in zip(meu_corpo, outro_corpo):
            if s1.obter_nome() != s2.obter_nome():
                return False

        # Compara a posição do ponto.
        return self.posicao_ponto == other.posicao_ponto

    def __hash__(self):

        # Cria uma tupla com os nomes dos símbolos do corpo para que seja hasheável.
        corpo_nomes = tuple(s.obter_nome() for s in self.producao.obter_corpo())
        return hash((self.producao.obter_cabeca(), corpo_nomes, self.posicao_ponto))
    def __str__(self):
        corpo_str = [s.obter_nome() for s in self.producao.obter_corpo()]
        
        if not corpo_str or corpo_str == ['&']:
            return f"{self.producao.obter_cabeca()} ::= ."
        
        corpo_str.insert(self.posicao_ponto, '.')
        return f"{self.producao.obter_cabeca()} ::= {' '.join(corpo_str)}"

   