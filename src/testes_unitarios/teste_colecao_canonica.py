import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Analisador_Sintatico.Gramatica import Gramatica
from Analisador_Sintatico.Simbolo import Simbolo
from Analisador_Sintatico.Producao import Producao
from Analisador_Sintatico.TipoSimbolo import TipoSimbolo
from Analisador_Sintatico.ItemLR0 import ItemLR0

def main():
    # Definição dos símbolos
    E_linha = "E'"
    E, T, F = 'E', 'T', 'F'
    mais, vezes, abre, fecha, id_ = '+', '*', '(', ')', 'id'

    nao_terminais = {E_linha, E, T, F}
    terminais = {mais, vezes, abre, fecha, id_}

    producoes = [
        Producao(E_linha, [Simbolo(E, TipoSimbolo.naoTerminal)]),
        Producao(E, [Simbolo(E, TipoSimbolo.naoTerminal), Simbolo(mais, TipoSimbolo.terminal), Simbolo(T, TipoSimbolo.naoTerminal)]),
        Producao(E, [Simbolo(T, TipoSimbolo.naoTerminal)]),
        Producao(T, [Simbolo(T, TipoSimbolo.naoTerminal), Simbolo(vezes, TipoSimbolo.terminal), Simbolo(F, TipoSimbolo.naoTerminal)]),
        Producao(T, [Simbolo(F, TipoSimbolo.naoTerminal)]),
        Producao(F, [Simbolo(abre, TipoSimbolo.terminal), Simbolo(E, TipoSimbolo.naoTerminal), Simbolo(fecha, TipoSimbolo.terminal)]),
        Producao(F, [Simbolo(id_, TipoSimbolo.terminal)]),
    ]
    gramatica = Gramatica(E_linha, nao_terminais, terminais, producoes)

    print("Gramática:")
    print(gramatica)
    print('---------------------')

    colecao, transicoes = gramatica.calcular_colecao_canonica()

    print("Coleção Canônica de Conjuntos de Itens LR(0):")
    for nome, conjunto in colecao:
        print(f"{nome}:")
        for item in sorted(conjunto, key=lambda x: str(x)):
            print(f"  {item}")
        print()

    print("Transições:")
    for (origem, simbolo), destino in sorted(transicoes.items()):
        print(f"{origem} -- {simbolo} --> {destino}")

if __name__ == "__main__":
    main()
