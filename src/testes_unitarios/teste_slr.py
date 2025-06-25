import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Analisador_Sintatico.SLR import SLRParser
from Analisador_Sintatico.Gramatica import Gramatica
from Analisador_Sintatico.Simbolo import Simbolo
from Analisador_Sintatico.Producao import Producao
from Analisador_Sintatico.TipoSimbolo import TipoSimbolo
from Analisador_Sintatico.ItemLR0 import ItemLR0
from Analisador_Sintatico.SLR import SLRParser 

def main():
    # Definição dos símbolos
    E_, E, T, F = "E'", 'E', 'T', 'F'
    mais, vezes, abre, fecha, id_ = '+', '*', '(', ')', 'id'

    nao_terminais = {E_, E, T, F}
    terminais = {mais, vezes, abre, fecha, id_}

    # Produções
    producoes = [
        Producao(E_, [Simbolo(E, TipoSimbolo.naoTerminal)]),
        Producao(E, [Simbolo(E, TipoSimbolo.naoTerminal), Simbolo(mais, TipoSimbolo.terminal), Simbolo(T, TipoSimbolo.naoTerminal)]),
        Producao(E, [Simbolo(T, TipoSimbolo.naoTerminal)]),
        Producao(T, [Simbolo(T, TipoSimbolo.naoTerminal), Simbolo(vezes, TipoSimbolo.terminal), Simbolo(F, TipoSimbolo.naoTerminal)]),
        Producao(T, [Simbolo(F, TipoSimbolo.naoTerminal)]),
        Producao(F, [Simbolo(abre, TipoSimbolo.terminal), Simbolo(E, TipoSimbolo.naoTerminal), Simbolo(fecha, TipoSimbolo.terminal)]),
        Producao(F, [Simbolo(id_, TipoSimbolo.terminal)]),
        ]

    # Instancia a gramática
    gramatica = Gramatica(E_, nao_terminais, terminais, producoes)

    # Coleção canônica e follow
    colecao_canonica, _ = gramatica.calcular_colecao_canonica()
    follow = gramatica.calcular_follow()

    # Criação do parser
    parser = SLRParser(gramatica, [conj for _, conj in colecao_canonica], follow)

    def imprimir_tabela_slr(parser):
        estados = sorted(set(i for (i, _) in parser.action.keys()) | set(i for (i, _) in parser.goto.keys()))
        terminais = sorted(set(s for (_, s) in parser.action.keys()))
        nao_terminais = sorted(set(s for (_, s) in parser.goto.keys()))

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
                acao = parser.action.get((estado, t))
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
                destino = parser.goto.get((estado, nt), '')
                linha.append(str(destino) if destino != '' else '')
            print(''.join(c.ljust(col_width) for c in linha))

    # Imprime a tabela SLR
    parser.imprimir_tabela()
    gramatica.imprimir_itens_canonicos()
    # Sentença de teste: id + id * id
    tokens = ['id', '+', 'id', '*', 'id']
    print(f"\nAnalisando: {' '.join(tokens)}")
    resultado = parser.parse(tokens)
    print("Resultado:", "Aceita" if resultado else "Rejeitada")



if __name__ == "__main__":
    main()