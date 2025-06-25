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

    # Definição das produções
    producoes = [
        Producao(E_linha, [Simbolo(E, TipoSimbolo.naoTerminal)]),
        Producao(E, [Simbolo(E, TipoSimbolo.naoTerminal), Simbolo(mais, TipoSimbolo.terminal), Simbolo(T, TipoSimbolo.naoTerminal)]),
        Producao(E, [Simbolo(T, TipoSimbolo.naoTerminal)]),
        Producao(T, [Simbolo(T, TipoSimbolo.naoTerminal), Simbolo(vezes, TipoSimbolo.terminal), Simbolo(F, TipoSimbolo.naoTerminal)]),
        Producao(T, [Simbolo(F, TipoSimbolo.naoTerminal)]),
        Producao(F, [Simbolo(abre, TipoSimbolo.terminal), Simbolo(E, TipoSimbolo.naoTerminal), Simbolo(fecha, TipoSimbolo.terminal)]),
        Producao(F, [Simbolo(id_, TipoSimbolo.terminal)]),
    ]

    # Instancia a gramática
    gramatica = Gramatica(E_linha, nao_terminais, terminais, producoes)

    print("Gramática:")
    print(gramatica)
    print('---------------------')

    # Item inicial: E′ → .E
    item_inicial = gramatica.criar_item_inicial()
    fecho = gramatica.calcular_fecho({item_inicial})

    print("Fecho do item [E′ → .E]:")
    for item in sorted(fecho, key=lambda x: str(x)):
        print(item)

if __name__ == "__main__":
    main()
