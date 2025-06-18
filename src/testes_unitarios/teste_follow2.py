import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Gramatica import Gramatica
from Simbolo import Simbolo
from Producao import Producao
from TipoSimbolo import TipoSimbolo

def main():
    S, A, B, C, D, E = 'S', 'A', 'B', 'C', 'D', 'E'
    nao_terminais = {S, A, B, C, D, E}
    terminais = {'a', 'b', 'c', 'd', 'e'}

    # Produções
    producoes = [
        Producao(S, [Simbolo(A, TipoSimbolo.naoTerminal), Simbolo(B, TipoSimbolo.naoTerminal), Simbolo(C, TipoSimbolo.naoTerminal)]),

        Producao(A, [Simbolo('a', TipoSimbolo.terminal), Simbolo(A, TipoSimbolo.naoTerminal)]),
        Producao(A, [Simbolo('&', TipoSimbolo.epsilon)]),

        Producao(B, [Simbolo('b', TipoSimbolo.terminal), Simbolo(B, TipoSimbolo.naoTerminal)]),
        Producao(B, [Simbolo(C, TipoSimbolo.naoTerminal), Simbolo(D, TipoSimbolo.naoTerminal)]),

        Producao(C, [Simbolo('c', TipoSimbolo.terminal), Simbolo(C, TipoSimbolo.naoTerminal)]),
        Producao(C, [Simbolo('&', TipoSimbolo.epsilon)]),

        Producao(D, [Simbolo('d', TipoSimbolo.terminal)]),
        Producao(D, [Simbolo(E, TipoSimbolo.naoTerminal)]),

        Producao(E, [Simbolo('e', TipoSimbolo.terminal)]),
        Producao(E, [Simbolo('&', TipoSimbolo.epsilon)])
    ]

    gramatica = Gramatica(inicial=S, nao_terminais=nao_terminais, terminais=terminais, producoes=producoes)

    print("FIRST:")
    first = gramatica.calcular_first()
    for nt in sorted(first):
        print(f"FIRST({nt}) = {{ {', '.join(sorted(first[nt]))} }}")

    print("\nFOLLOW:")
    follow = gramatica.calcular_follow()
    for nt in sorted(follow):
        print(f"FOLLOW({nt}) = {{ {', '.join(sorted(follow[nt]))} }}")


if __name__ == "__main__":
    main()
