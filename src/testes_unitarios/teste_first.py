import sys
import os
sys.path.append(os.path.abspath('..'))

from Gramatica import Gramatica
from Producao import Producao
from Simbolo import Simbolo
from TipoSimbolo import TipoSimbolo


def main():
    # Não terminais
    E = 'E'
    T = 'T'
    F = 'F'

    nao_terminais = {E, T, F}
    terminais = {'+', '*', '(', ')', 'id'}

    producoes = [
        Producao(E, [Simbolo(T, TipoSimbolo.naoTerminal)]),
        Producao(E, [Simbolo(E, TipoSimbolo.naoTerminal), Simbolo('+', TipoSimbolo.terminal), Simbolo(T, TipoSimbolo.naoTerminal)]),
        Producao(T, [Simbolo(F, TipoSimbolo.naoTerminal)]),
        Producao(T, [Simbolo(T, TipoSimbolo.naoTerminal), Simbolo('*', TipoSimbolo.terminal), Simbolo(F, TipoSimbolo.naoTerminal)]),
        Producao(F, [Simbolo('(', TipoSimbolo.terminal), Simbolo(E, TipoSimbolo.naoTerminal), Simbolo(')', TipoSimbolo.terminal)]),
        Producao(F, [Simbolo('id', TipoSimbolo.terminal)])
    ]

    gramatica = Gramatica(inicial=E, nao_terminais=nao_terminais, terminais=terminais, producoes=producoes)

    first = gramatica.calcular_first()

    for nt, conjunto in first.items():
        print(f"FIRST({nt}) = {{ {', '.join(conjunto)} }}")


if __name__ == "__main__":
    main()
