from TipoSimbolo import TipoSimbolo
from ItemLR0 import ItemLR0

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


    def calcular_follow(self):
        # Inicializa o conjunto FOLLOW para cada não terminal como um conjunto vazio
        follow = {nt: set() for nt in self.nao_terminais}
        
        # Regra 1: adiciona $ ao FOLLOW do símbolo inicial
        follow[self.inicial].add('$')

        # Calcula o conjunto FIRST para uso posterior
        first = self.calcular_first() 

        mudou = True
        while mudou:
            mudou = False

            for producao in self.producoes:
                cabeca = producao.obter_cabeca()  
                corpo = producao.obter_corpo()    

                for i in range(len(corpo)):
                    simbolo = corpo[i]

                    # Só aplicamos regras de FOLLOW para não terminais
                    if simbolo.obter_tipo() != TipoSimbolo.naoTerminal:
                        continue

                    B = simbolo.obter_nome()

                    # Regra 2: A ::= α B β → tudo que está em FIRST(β) vai para FOLLOW(B)
                    if i + 1 < len(corpo):  # Existe β
                        beta = corpo[i+1:]  

                        # Calcula FIRST(β)
                        first_beta = set()
                        epsilon_em_tudo = True

                        for s in beta:
                            tipo = s.obter_tipo()
                            nome = s.obter_nome()

                            if tipo == TipoSimbolo.terminal:
                                first_beta.add(nome)
                                epsilon_em_tudo = False
                                break

                            elif tipo == TipoSimbolo.naoTerminal:
                                first_beta.update([x for x in first[nome] if x != '&'])
                                if '&' not in first[nome]:
                                    epsilon_em_tudo = False
                                    break
                            elif tipo == TipoSimbolo.epsilon:
                                first_beta.add('&')
                                break

                        # Adiciona FIRST(β) \ {ε} em FOLLOW(B)
                        antes = len(follow[B])
                        follow[B].update(first_beta - {'&'})
                        if len(follow[B]) > antes:
                            mudou = True

                        # Regra 3: se FIRST(β) contém ε, então FOLLOW(A) vai para FOLLOW(B)
                        if epsilon_em_tudo:
                            antes = len(follow[B])
                            follow[B].update(follow[cabeca])
                            if len(follow[B]) > antes:
                                mudou = True

                    else:
                        # Regra 3: A ::= α B → FOLLOW(A) vai para FOLLOW(B)
                        antes = len(follow[B])
                        follow[B].update(follow[cabeca])
                        if len(follow[B]) > antes:
                            mudou = True

        return follow

    def obter_producoes(self):
        return self.producoes
    
    def obter_nao_terminais(self):
        return self.nao_terminais
    
    def obter_terminais(self):
        return self.terminais
    
    def obter_inicial(self):
        return self.inicial
    
    def __str__(self):
        linhas = []
        linhas.append(f"Símbolo inicial: {self.inicial}")
        linhas.append(f"Não-terminais: {', '.join(sorted(self.nao_terminais))}")
        linhas.append(f"Terminais: {', '.join(sorted(self.terminais))}")
        linhas.append("Produções:")

        # Agrupa produções por cabeça
        producoes_por_cabeca = {}
        for p in self.producoes:
            cabeca = p.obter_cabeca()
            corpo = p.obter_corpo()
            corpo_str = ' '.join(s.obter_nome() for s in corpo)
            if cabeca not in producoes_por_cabeca:
                producoes_por_cabeca[cabeca] = []
            producoes_por_cabeca[cabeca].append(corpo_str)

        # Garante que o símbolo inicial venha primeiro
        ordem_cabecas = [self.inicial] + sorted(nt for nt in producoes_por_cabeca if nt != self.inicial)

        for cabeca in ordem_cabecas:
            if cabeca in producoes_por_cabeca:
                corpos = producoes_por_cabeca[cabeca]
                linha = f"  {cabeca} ::= {' | '.join(corpos)}"
                linhas.append(linha)

        return '\n'.join(linhas)


    from ItemLR0 import ItemLR0

    def criar_item_inicial(self):
        simbolo_inicial = self.obter_inicial()
        for producao in self.obter_producoes():
            if producao.obter_cabeca() == simbolo_inicial:
                return ItemLR0(producao, 0)
        raise ValueError(f"Nenhuma produção encontrada com cabeça {simbolo_inicial}")


    # Closure de um item LR(0)
    def calcular_fecho(self, itens_I): 
            fecho = set(itens_I)
            adicionado = True
            while adicionado:
                adicionado = False
                novos_itens = set()
                for item in fecho:
                    # Pega o símbolo B logo após o ponto na produção [A ::= α.Bβ]
                    simbolo_B = item.obter_simbolo_apos_ponto()
                    
                    # Se B for um não-terminal...
                    if simbolo_B and simbolo_B.obter_tipo() == TipoSimbolo.naoTerminal:
                        nome_B = simbolo_B.obter_nome()
                        # ...para cada produção B ::= γ...
                        for prod in self.producoes:
                            if prod.obter_cabeca() == nome_B:
                                # ...adiciona o item [B ::= .γ] ao fecho.
                                novo_item = ItemLR0(prod, 0)
                                if novo_item not in fecho and novo_item not in novos_itens:
                                    novos_itens.add(novo_item)
                                    adicionado = True
                fecho.update(novos_itens)
                
            return fecho