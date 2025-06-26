from Analisador_Sintatico.TipoSimbolo import TipoSimbolo
from Analisador_Sintatico.Simbolo import Simbolo
from Analisador_Sintatico.Producao import Producao
from Analisador_Sintatico.ItemLR0 import ItemLR0

class Gramatica:
    def __init__(self, simbolo_inicial, nao_terminais, terminais, producoes):
       
        simbolo_inicial_aumentado = simbolo_inicial + "'"
        
        nao_terminais.add(simbolo_inicial_aumentado)
        
        simbolo_inicial_obj = Simbolo(simbolo_inicial, TipoSimbolo.naoTerminal)
        producao_aumentada = Producao(simbolo_inicial_aumentado, [simbolo_inicial_obj])
        
        producoes.insert(0, producao_aumentada)

        self.inicial = simbolo_inicial_aumentado
        self.nao_terminais = nao_terminais
        self.terminais = terminais
        self.producoes = producoes
        
    def calcular_first(self):
        # Inicializa o conjunto FIRST para cada não terminal com um conjunto vazio.

        first = {nt: set() for nt in self.nao_terminais}
        
        mudou = True
        while mudou:
            mudou = False
            for producao in self.producoes:
                cabeca = producao.obter_cabeca()
                corpo = producao.obter_corpo()

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
                    
                    # Se X ::=ε∈P,então ε ∈ FIRST(X)
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

    def criar_item_inicial(self):
        producao_inicial_aumentada = self.obter_producoes()[0]
        # Confirma se a produção é a correta
        if producao_inicial_aumentada.obter_cabeca() == self.inicial:
            return ItemLR0(producao_inicial_aumentada, 0)

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
    
    def calcular_colecao_canonica(self):
        simbolos = list(self.nao_terminais | self.terminais)
        item_inicial = self.criar_item_inicial()
        I0 = frozenset(self.calcular_fecho({item_inicial}))
        colecao = [I0]
        nomes = {I0: 'I0'}
        transicoes = {}
        fila = [I0]
        contador = 1
        while fila:
            estado = fila.pop(0)
            for simbolo in simbolos:
                itens_avancados = set()
                for item in estado:
                    prox = item.obter_simbolo_apos_ponto()
                    if prox and prox.obter_nome() == simbolo:
                        itens_avancados.add(item.avancar_ponto())
                if itens_avancados:
                    fecho = frozenset(self.calcular_fecho(itens_avancados))
                    if fecho not in nomes:
                        nomes[fecho] = f"I{contador}"
                        colecao.append(fecho)
                        fila.append(fecho)
                        contador += 1
                    transicoes[(nomes[estado], simbolo)] = nomes[fecho]
            
        return [(nomes[conj], conj) for conj in colecao], transicoes

    def imprimir_itens_canonicos(self):
        colecao, _ = self.calcular_colecao_canonica()
        print("\nCOLEÇÃO CANÔNICA DE ITENS LR(0):\n")
        for nome_estado, conjunto in colecao:
            print(f"{nome_estado}:")
            for item in sorted(conjunto, key=lambda x: str(x)):
                print(f"  {item}")
            print("-" * 40)


    def obter_colecao_canonica(self):
        colecao, _ = self.calcular_colecao_canonica()
        return colecao

    def obter_inicial(self):
        return self.inicial
    
    def obter_nao_terminais(self):
        return self.nao_terminais
    
    def obter_terminais(self):
        return self.terminais
    
    def obter_producoes(self):
        return self.producoes