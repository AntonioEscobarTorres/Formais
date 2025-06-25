import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Analisador_Sintatico.Gramatica import Gramatica
from Analisador_Sintatico.Simbolo import Simbolo
from Analisador_Sintatico.Producao import Producao
from Analisador_Sintatico.TipoSimbolo import TipoSimbolo
from Analisador_Sintatico.ItemLR0 import ItemLR0

def main():
    # Símbolos
    Sprime = "S'"
    S, C = "S", "C"
    c, d = "c", "d"

    nao_terminais = {Sprime, S, C}
    terminais = {c, d}

    producoes = [
        Producao(Sprime, [Simbolo(S, TipoSimbolo.naoTerminal)]),
        Producao(S, [Simbolo(C, TipoSimbolo.naoTerminal), Simbolo(C, TipoSimbolo.naoTerminal)]),
        Producao(C, [Simbolo(c, TipoSimbolo.terminal), Simbolo(C, TipoSimbolo.naoTerminal)]),
        Producao(C, [Simbolo(d, TipoSimbolo.terminal)])
    ]

    gramatica = Gramatica(Sprime, nao_terminais, terminais, producoes)

    print("Gramática:")
    print(gramatica)
    print('---------------------')

    item_inicial = gramatica.criar_item_inicial()
    fecho = gramatica.calcular_fecho({item_inicial})

    print("Fecho do item [S′ → .S]:")
    simbolo_inicial = Sprime
    for item in sorted(fecho, key=lambda x: (x.producao.obter_cabeca() != simbolo_inicial, str(x))):
        print(item)

if __name__ == "__main__":
    main()
