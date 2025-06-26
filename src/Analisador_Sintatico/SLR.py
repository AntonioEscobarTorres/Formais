from Analisador_Sintatico.TipoSimbolo import TipoSimbolo

class SLRParser:
    def __init__(self, gramatica, colecao_canonica, follow):
        self.gramatica = gramatica
        self.colecao_canonica = colecao_canonica  # List[frozenset[ItemLR0]]
        self.follow = follow                      # Dict[str, Set[str]]
        self.action = {}
        self.goto = {}
        self._construir_tabela_slr()

    def _construir_tabela_slr(self):
        terminais = self.gramatica.obter_terminais().union({'$'})
        nao_terminais = self.gramatica.obter_nao_terminais()

        producoes = self.gramatica.obter_producoes()

        for i, I in enumerate(self.colecao_canonica):

            for item in I:
                prod = item.obter_producao()
                cabeca = prod.obter_cabeca()
                corpo = prod.obter_corpo()
                ponto = item.obter_posicao_ponto()

                simbolo_apos = item.obter_simbolo_apos_ponto()

                # CASO SHIFT: [A → α . a β] e 'a' terminal
                if simbolo_apos and simbolo_apos.obter_tipo() == TipoSimbolo.terminal:
                    simbolo_nome = simbolo_apos.obter_nome()
                    j = self._estado_destino(I, simbolo_nome)
                    if j is not None:
                        self.action[(i, simbolo_nome)] = ('shift', j)

                # CASO REDUCE ou ACCEPT
                elif item.esta_completo():
                    # ACCEPT: produção inicial e símbolo de final
                    if cabeca == self.gramatica.obter_inicial():
                        self.action[(i, '$')] = ('accept',)
                    else:
                        # REDUCE para todos os símbolos em FOLLOW(cabeca)
                        prod_idx = producoes.index(prod)
                        for terminal in self.follow.get(cabeca, []):
                            self.action[(i, terminal)] = ('reduce', prod_idx)

            # GOTO: para cada não-terminal A
            for A in nao_terminais:
                j = self._estado_destino(I, A)
                if j is not None:
                    self.goto[(i, A)] = j

    def _estado_destino(self, I, simbolo_nome):
        """
        Determina o estado alcançado ao fazer transição com 'simbolo_nome' a partir de estado 'I'
        """
        itens_avancados = set()
        for item in I:
            simbolo_apos = item.obter_simbolo_apos_ponto()
            if simbolo_apos and simbolo_apos.obter_nome() == simbolo_nome:
                itens_avancados.add(item.avancar_ponto())
        if not itens_avancados:

            return None

        fecho = frozenset(self.gramatica.calcular_fecho(itens_avancados))
        for j, estado in enumerate(self.colecao_canonica):
            if fecho == estado:

                return j
        return None

    def parse(self, tokens):
        pilha = [0]
        entrada = tokens + ['$']
        ponteiro = 0 # Usando um ponteiro em vez de pop(0)

        while True:

            s = pilha[-1]
            a = entrada[ponteiro]

            acao = self.action.get((s, a))

            if acao is None:
                print(f"Erro de sintaxe: Nenhuma ação para estado={s}, token='{a}'")
                return False

            if acao[0] == 'shift':
                pilha.append(acao[1])
                ponteiro += 1

            elif acao[0] == 'reduce':
                prod_idx = acao[1]
                prod = self.gramatica.obter_producoes()[prod_idx]
                
                if prod.obter_corpo() and prod.obter_corpo()[0].obter_nome() != '&':
                    for _ in prod.obter_corpo():
                        if pilha:
                            pilha.pop()
                        else:
                            print("!!! ERRO: Tentativa de pop em pilha vazia durante reduce!")
                            return False

                if not pilha:
                    print("!!! ERRO: Pilha ficou vazia após o reduce!")
                    return False

                t = pilha[-1]
                pilha.append(self.goto[(t, prod.obter_cabeca())])

            elif acao[0] == 'accept':
                print("Oii")
                print("Sentença aceita!")
                return True


    def imprimir_tabela(self):
        estados = sorted(set(i for (i, _) in self.action.keys()) | set(i for (i, _) in self.goto.keys()))
        terminais = sorted(set(s for (_, s) in self.action.keys()))
        nao_terminais = sorted(set(s for (_, s) in self.goto.keys()))

        print("\nTABELA DE ANÁLISE SLR(1)\n")

        # Cabeçalho
        cabecalho = ['Estado'] + terminais + nao_terminais
        col_width = max(len(str(c)) for c in cabecalho) + 2
        linha_formatada = ''.join(c.ljust(col_width) for c in cabecalho)
        print(linha_formatada)
        print('-' * len(linha_formatada))

        for estado in estados:
            linha = [str(estado)]
            # ACTION
            for t in terminais:
                acao = self.action.get((estado, t))
                if acao is None:
                    linha.append('')
                elif acao[0] == 'shift':
                    linha.append(f's{acao[1]}')
                elif acao[0] == 'reduce':
                    linha.append(f'r{acao[1]}')
                elif acao[0] == 'accept':
                    linha.append('acc')
                else:
                    linha.append('?')
            # GOTO
            for nt in nao_terminais:
                destino = self.goto.get((estado, nt), '')
                linha.append(str(destino) if destino != '' else '')
            print(''.join(c.ljust(col_width) for c in linha))