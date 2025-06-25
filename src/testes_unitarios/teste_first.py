import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Analisador_Sintatico.Gramatica import Gramatica
from Analisador_Sintatico.Producao import Producao
from Analisador_Sintatico.Simbolo import Simbolo
from Analisador_Sintatico.TipoSimbolo import TipoSimbolo


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
