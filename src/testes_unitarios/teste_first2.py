import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from Analisador_Sintatico.Gramatica import Gramatica
from Analisador_Sintatico.Producao import Producao
from Analisador_Sintatico.Simbolo import Simbolo
from Analisador_Sintatico.TipoSimbolo import TipoSimbolo


def main():
    # Não terminais
    S = 'S'
    A = 'A'
    B = 'B'
    C = 'C'

    nao_terminais = {S, A, B, C}
    terminais = {'a', 'b', 'c', 'd'}

    producoes = [
        Producao(S, [Simbolo(A, TipoSimbolo.naoTerminal), Simbolo(B, TipoSimbolo.naoTerminal), Simbolo(C, TipoSimbolo.naoTerminal)]),
        Producao(A, [Simbolo('a', TipoSimbolo.terminal), Simbolo(A, TipoSimbolo.naoTerminal)]),
        Producao(A, [Simbolo('&', TipoSimbolo.epsilon)]),
        Producao(B, [Simbolo('b', TipoSimbolo.terminal), Simbolo(B, TipoSimbolo.naoTerminal)]),
        Producao(B, [Simbolo(A, TipoSimbolo.naoTerminal), Simbolo(C, TipoSimbolo.naoTerminal), Simbolo('d', TipoSimbolo.terminal)]),
        Producao(C, [Simbolo('c', TipoSimbolo.terminal), Simbolo(C, TipoSimbolo.naoTerminal)]),
        Producao(C, [Simbolo('&', TipoSimbolo.epsilon)]),
    ]

    gramatica = Gramatica(inicial=S, nao_terminais=nao_terminais, terminais=terminais, producoes=producoes)

    first = gramatica.calcular_first()

    for nt, conjunto in first.items():
        print(f"FIRST({nt}) = {{ {', '.join(conjunto)} }}")


if __name__ == "__main__":
    main()
