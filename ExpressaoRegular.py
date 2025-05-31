from Automato import Automato
from Estado import Estado
from Transicao import Transicao

class NodoER:
    def __init__(self, valor, esquerda=None, direita=None):
        self.valor = valor
        self.esquerda = esquerda
        self.direita = direita
        self.nullable = False
        self.firstpos = set()
        self.lastpos = set()
        self.pos = None  # Só para folhas
        self.followpos = set()  # Só para folhas

class ExpressaoRegular:
    def __init__(self, er):
        self.er = er
        self.simbolos = set()
        self.pos_to_symbol = {}
        self.followpos_table = {}
        self.root = None

    def infixa_para_posfixa(self, expr):
        precedencia = {'*': 3, '.': 2, '|': 1}
        output = []
        stack = []
        # Inserir concatenação explícita de forma robusta
        nova_expr = ""
        prev = None
        for c in expr:
            if c == ' ':
                continue
            if prev:
                # Se prev é símbolo, ')' ou '*', e c é símbolo ou '(', insere '.'
                if ((prev not in {'(', '|'} and prev is not None) and
                    (c not in {'|', ')', '*'})):
                    nova_expr += '.'
            nova_expr += c
            prev = c
        expr = nova_expr

        # Validação de parênteses
        count_par = 0
        for c in expr:
            if c == '(':
                count_par += 1
            elif c == ')':
                count_par -= 1
            if count_par < 0:
                raise ValueError("Parênteses desbalanceados na expressão regular.")
        if count_par != 0:
            raise ValueError("Parênteses desbalanceados na expressão regular.")

        for c in expr:
            if c == '(':
                stack.append(c)
            elif c == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack:
                    raise ValueError("Parênteses desbalanceados na expressão regular.")
                stack.pop()
            elif c in precedencia:
                while (stack and stack[-1] != '(' and
                       precedencia.get(stack[-1], 0) >= precedencia[c]):
                    output.append(stack.pop())
                stack.append(c)
            else:
                output.append(c)
        while stack:
            if stack[-1] == '(' or stack[-1] == ')':
                raise ValueError("Parênteses desbalanceados na expressão regular.")
            output.append(stack.pop())
        return output

    def construir_arvore(self, posfixa):
        stack = []
        pos = 1
        for c in posfixa:
            if c not in {'*', '.', '|'}:
                nodo = NodoER(c)
                nodo.pos = pos
                pos += 1
                stack.append(nodo)
            elif c == '*':
                filho = stack.pop()
                nodo = NodoER('*', esquerda=filho)
                stack.append(nodo)
            elif c == '.':
                direita = stack.pop()
                esquerda = stack.pop()
                nodo = NodoER('.', esquerda, direita)
                stack.append(nodo)
            elif c == '|':
                direita = stack.pop()
                esquerda = stack.pop()
                nodo = NodoER('|', esquerda, direita)
                stack.append(nodo)
        return stack[0], pos-1

    def calcular_nullable_first_last(self, nodo):
        if nodo is None:
            return
        if nodo.valor not in {'*', '.', '|'}:
            nodo.nullable = False
            nodo.firstpos = {nodo.pos}
            nodo.lastpos = {nodo.pos}
        elif nodo.valor == '|':
            self.calcular_nullable_first_last(nodo.esquerda)
            self.calcular_nullable_first_last(nodo.direita)
            nodo.nullable = nodo.esquerda.nullable or nodo.direita.nullable
            nodo.firstpos = nodo.esquerda.firstpos | nodo.direita.firstpos
            nodo.lastpos = nodo.esquerda.lastpos | nodo.direita.lastpos
        elif nodo.valor == '.':
            self.calcular_nullable_first_last(nodo.esquerda)
            self.calcular_nullable_first_last(nodo.direita)
            nodo.nullable = nodo.esquerda.nullable and nodo.direita.nullable
            if nodo.esquerda.nullable:
                nodo.firstpos = nodo.esquerda.firstpos | nodo.direita.firstpos
            else:
                nodo.firstpos = nodo.esquerda.firstpos
            if nodo.direita.nullable:
                nodo.lastpos = nodo.esquerda.lastpos | nodo.direita.lastpos
            else:
                nodo.lastpos = nodo.direita.lastpos
        elif nodo.valor == '*':
            self.calcular_nullable_first_last(nodo.esquerda)
            nodo.nullable = True
            nodo.firstpos = nodo.esquerda.firstpos
            nodo.lastpos = nodo.esquerda.lastpos

    def calcular_followpos(self, nodo, followpos_table):
        if nodo is None:
            return
        if nodo.valor == '.':
            for i in nodo.esquerda.lastpos:
                followpos_table.setdefault(i, set()).update(nodo.direita.firstpos)
        if nodo.valor == '*':
            for i in nodo.lastpos:
                followpos_table.setdefault(i, set()).update(nodo.firstpos)
        self.calcular_followpos(nodo.esquerda, followpos_table)
        self.calcular_followpos(nodo.direita, followpos_table)

    def construir_afd(self):
        # Passo 1: ER para pós-fixa
        expr = f'({self.er})#'
        posfixa = self.infixa_para_posfixa(expr)
        # Passo 2: árvore sintática
        self.root, total_pos = self.construir_arvore(posfixa)
        # Passo 3: nullable, firstpos, lastpos
        self.calcular_nullable_first_last(self.root)
        # Passo 4: followpos
        self.followpos_table = {}
        self.calcular_followpos(self.root, self.followpos_table)
        # Mapear posições para símbolos
        def mapear_posicoes(nodo):
            if nodo is None:
                return
            if nodo.valor not in {'*', '.', '|'}:
                self.pos_to_symbol[nodo.pos] = nodo.valor
                if nodo.valor not in {'#'}:
                    self.simbolos.add(nodo.valor)
            mapear_posicoes(nodo.esquerda)
            mapear_posicoes(nodo.direita)
        mapear_posicoes(self.root)
        # Passo 5: Construção do AFD
        estados = []
        estados_map = {}
        fila = []
        transicoes = []  # Nova lista para armazenar as transições
        estado_inicial = frozenset(self.root.firstpos)
        estados.append(estado_inicial)
        estados_map[estado_inicial] = Estado(str(estado_inicial))
        fila.append(estado_inicial)
        finais = set()
        while fila:
            atual = fila.pop(0)
            estado_atual = estados_map[atual]
            if any(self.pos_to_symbol[p] == '#' for p in atual):
                estado_atual.final = True
                finais.add(estado_atual)
            for simbolo in self.simbolos:
                prox = set()
                for p in atual:
                    if self.pos_to_symbol[p] == simbolo:
                        prox.update(self.followpos_table.get(p, set()))
                if prox:
                    prox_frozen = frozenset(prox)
                    if prox_frozen not in estados_map:
                        novo_estado = Estado(str(prox_frozen))
                        estados_map[prox_frozen] = novo_estado
                        estados.append(prox_frozen)
                        fila.append(prox_frozen)
                    else:
                        novo_estado = estados_map[prox_frozen]
                    trans = Transicao(estado_atual, simbolo, novo_estado)
                    transicoes.append(trans)  # Armazene aqui
        automato = Automato(
            len(estados_map),  # n_estados
            estados_map[estado_inicial],  # inicial
            finais,  # finais (set de Estado)
            set(transicoes),  # transicoes (set de Transicao)
            self.simbolos  # alfabeto (set de str)
        )
        return automato
