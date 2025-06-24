class SLRParser:
    def __init__(self, gramatica, colecao_canonica, follow):
        self.gramatica = gramatica
        self.colecao_canonica = colecao_canonica  # Lista de conjuntos de itens LR(0)
        self.follow = follow
        self.action = {}
        self.goto = {}
        self._construir_tabela_slr()

    def _construir_tabela_slr(self):
        terminais = set()
        nao_terminais = set()
        for prod in self.gramatica.producoes:
            terminais.update([x for x in prod['corpo'] if not x.isupper()])
            nao_terminais.add(prod['cabeca'])
        terminais.add('$')

        # Mapeia produções para índices
        prod_map = []
        for idx, prod in enumerate(self.gramatica.producoes):
            prod_map.append((prod['cabeca'], tuple(prod['corpo'])))

        for i, I in enumerate(self.colecao_canonica):
            # ACTION
            for item in I:
                cabeca = item['cabeca']
                corpo = item['corpo']
                ponto = item['ponto']
                # Caso 1: item é [A -> α . a β], a é terminal
                if ponto < len(corpo):
                    a = corpo[ponto]
                    if a in terminais and a != '&':
                        j = self._ir_para(i, a)
                        if j is not None:
                            self.action[(i, a)] = ('shift', j)
                # Caso 2: item é [A -> α .], ponto no fim
                else:
                    if cabeca == self.gramatica.producoes[0]['cabeca']:
                        # Produção inicial aumentada
                        self.action[(i, '$')] = ('accept',)
                    else:
                        # Reduce para cada símbolo em FOLLOW(A)
                        prod_idx = self._indice_producao(cabeca, corpo)
                        for a in self.follow[cabeca]:
                            self.action[(i, a)] = ('reduce', prod_idx)
            # GOTO
            for A in nao_terminais:
                j = self._ir_para(i, A)
                if j is not None:
                    self.goto[(i, A)] = j

    def _ir_para(self, i, X):
        if not self.colecao_canonica or i >= len(self.colecao_canonica):
            return None
        I = self.colecao_canonica[i]
        prox = []
        for item in I:
            corpo = item['corpo']
            ponto = item['ponto']
            if ponto < len(corpo) and corpo[ponto] == X:
                prox.append({'cabeca': item['cabeca'], 'corpo': corpo, 'ponto': ponto + 1})
        if not prox:
            return None
        # Busca o conjunto igual na coleção canônica (agora aceita subconjunto)
        for j, J in enumerate(self.colecao_canonica):
            if set((item['cabeca'], tuple(item['corpo']), item['ponto']) for item in prox).issubset(
                set((item['cabeca'], tuple(item['corpo']), item['ponto']) for item in J)
            ):
                return j
        return None

    def _mesmo_conjunto(self, I, J):
        # Compara dois conjuntos de itens (listas de dicts)
        return set((item['cabeca'], tuple(item['corpo']), item['ponto']) for item in I) == \
               set((item['cabeca'], tuple(item['corpo']), item['ponto']) for item in J)

    def _indice_producao(self, cabeca, corpo):
        # Retorna o índice da produção (cabeca, corpo) na lista de produções
        for idx, prod in enumerate(self.gramatica.producoes):
            if prod['cabeca'] == cabeca and list(prod['corpo']) == list(corpo):
                return idx
        raise Exception(f"Produção não encontrada: {cabeca} -> {corpo}")

    def parse(self, tokens):
        # Algoritmo 4.44: parsing LR
        pilha = [0]
        entrada = tokens + ['$']
        a = entrada.pop(0)
        while True:
            s = pilha[-1]
            acao = self.action.get((s, a))
            if acao is None:
                print(f"Erro de sintaxe: estado={s}, token={a}")
                return False
            if acao[0] == 'shift':
                pilha.append(acao[1])
                a = entrada.pop(0)
            elif acao[0] == 'reduce':
                prod = self.gramatica.producoes[acao[1]]
                for _ in prod['corpo']:
                    pilha.pop()
                t = pilha[-1]
                pilha.append(self.goto[(t, prod['cabeca'])])
                print(f"Reduce: {prod['cabeca']} -> {' '.join(prod['corpo'])}")
            elif acao[0] == 'accept':
                print("Sentença aceita!")
                return True
            else:
                print("Erro de sintaxe")
                return False