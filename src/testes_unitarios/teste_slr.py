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