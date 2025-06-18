from TipoSimbolo import TipoSimbolo

class Gramatica:
    def __init__(self, inicial, nao_terminais, terminais, producoes):
        self.nao_terminais = nao_terminais
        self.terminais = terminais
        self.producoes = producoes
        self.inicial = inicial

        
    def calcular_first(self):
        # Inicializa o conjunto FIRST para cada não terminal
        # com um conjunto vazio.
        first = {nt: set() for nt in self.nao_terminais}
        
        mudou = True
        #
        while mudou:
            mudou = False
            for producao in self.producoes:
                cabeca = producao.obter_cabeca()
                corpo = producao.obter_corpo()  # Supondo que corpo é uma lista de símbolos

                adicionou_epsilon = True

                # Percorre cada símbolo no corpo da produção
                for simbolo in corpo:
                    tipo = simbolo.obter_tipo()
                    nome = simbolo.obter_nome()

                    # Se o símbolo é terminal, adiciona ao conjunto FIRST
                    # e para o loop, pois não há mais símbolos a processar.
                    # do algo: 1.Se X ∈ T então FIRST(X) ={X}
                    if tipo == TipoSimbolo.terminal:
                        if nome not in first[cabeca]:
                            first[cabeca].add(nome)
                            mudou = True
                        adicionou_epsilon = False
                        break


                    # 2. Se X ∈ N então
                    # Se o símbolo é não terminal, adiciona os símbolos do conjunto FIRST
                    # do não terminal ao conjunto FIRST da cabeça da produção.
                    
                    elif tipo == TipoSimbolo.naoTerminal:
                        for s in first[simbolo.obter_nome()]:
                            if s != '&' and s not in first[cabeca]:
                                first[cabeca].add(s)
                                mudou = True
                        if '&' not in first[simbolo.obter_nome()]:
                            adicionou_epsilon = False
                            break
                    
                    # 2b Se X ::=ε∈P,entãoε∈FIRST(X)
                    # Se o símbolo é epsilon, adiciona epsilon ao conjunto FIRST
                    elif tipo == TipoSimbolo.epsilon:
                        if '&' not in first[cabeca]:
                            first[cabeca].add('&')
                            mudou = True
                        adicionou_epsilon = False
                        break

                # Se todos os símbolos do corpo são não terminais e
                # o último símbolo é epsilon, adiciona epsilon ao conjunto FIRST
                # da cabeça da produção.
                # Isso acontece quando o corpo é vazio ou contém apenas não terminais
                if adicionou_epsilon:
                    if '&' not in first[cabeca]:
                        first[cabeca].add('&')
                        mudou = True

        return first
