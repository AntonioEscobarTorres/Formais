import sys
import os
from pprint import pprint

# Adiciona o diretório pai ao path para permitir os imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Imports das suas classes de definição da gramática e do parser
from Analisador_Sintatico.Gramatica import Gramatica
from Analisador_Sintatico.Simbolo import Simbolo
from Analisador_Sintatico.Producao import Producao
from Analisador_Sintatico.TipoSimbolo import TipoSimbolo
from Analisador_Sintatico.SLR import SLRParser


def main():

    print("--- 1. Gerando dados a partir da classe Gramatica ---")
    
    # Definição dos símbolos
    E_linha, E, T, F = "E'", 'E', 'T', 'F'
    mais, vezes, abre, fecha, id_ = '+', '*', '(', ')', 'id'

    nao_terminais = {E_linha, E, T, F}
    terminais = {mais, vezes, abre, fecha, id_}

    producoes_obj = [
        Producao(E_linha, [Simbolo(E, TipoSimbolo.naoTerminal)]),
        Producao(E, [Simbolo(E, TipoSimbolo.naoTerminal), Simbolo(mais, TipoSimbolo.terminal), Simbolo(T, TipoSimbolo.naoTerminal)]),
        Producao(E, [Simbolo(T, TipoSimbolo.naoTerminal)]),
        Producao(T, [Simbolo(T, TipoSimbolo.naoTerminal), Simbolo(vezes, TipoSimbolo.terminal), Simbolo(F, TipoSimbolo.naoTerminal)]),
        Producao(T, [Simbolo(F, TipoSimbolo.naoTerminal)]),
        Producao(F, [Simbolo(abre, TipoSimbolo.terminal), Simbolo(E, TipoSimbolo.naoTerminal), Simbolo(fecha, TipoSimbolo.terminal)]),
        Producao(F, [Simbolo(id_, TipoSimbolo.terminal)]),
    ]

    gramatica = Gramatica(E_linha, nao_terminais, terminais, producoes_obj)
    
    # Geração da coleção canônica e do conjunto FOLLOW
    colecao_gerada, _ = gramatica.calcular_colecao_canonica()
    follow_gerado = gramatica.calcular_follow() # Assumindo que sua classe tem este método

    print("Geração concluída.\n")

    # --------------------------------------------------------------------------
    # 2. Transformação dos Dados para o Formato do Parser
    # --------------------------------------------------------------------------
    print("--- 2. Transformando dados para o formato do SLRParser ---")

    colecao_transformada = gramatica.obter_colecao_formato_parser()
    producoes_transformadas = gramatica.obter_producoes_formato_parser()
    # Mock da gramática para o parser, usando as produções transformadas
    gramatica_para_parser = type('G', (), {'producoes': producoes_transformadas})()

    print("Transformação concluída. Exemplo de estado (I0) para o parser:")
    pprint(colecao_transformada[0])
    print("\n")

    # --------------------------------------------------------------------------
    # 3. Instanciação e Teste do Parser
    # --------------------------------------------------------------------------
    print("--- 3. Instanciando e executando testes no SLRParser ---")
    
    # Instanciando o parser com os dados gerados e transformados
    parser = SLRParser(gramatica_para_parser, colecao_transformada, follow_gerado)
    
    # Lista de testes PARA A GRAMÁTICA DE EXPRESSÕES
    testes = [
        (['id', '+', 'id'], "Válido: Soma simples"),
        (['id', '*', 'id'], "Válido: Multiplicação simples"),
        (['(', 'id', ')'], "Válido: Parênteses simples"),
        (['id', '+', 'id', '*', 'id'], "Válido: Expressão mista"),
        (['(', 'id', '+', 'id', ')', '*', 'id'], "Válido: Expressão com precedência"),
        (['id'], "Válido: Apenas um identificador"),
        (['id', '+'], "Inválido: Operação incompleta"),
        (['(', 'id', '+', 'id'], "Inválido: Falta fechar parênteses"),
        (['id', '+', '+', 'id'], "Inválido: Operadores consecutivos"),
        (['id', 'id'], "Inválido: Identificadores consecutivos"),
        ([], "Inválido: Entrada vazia"),
    ]

    # Rodando os testes
    for tokens, descricao in testes:
        print(f"\nTeste - {descricao}: Entrada: {tokens}")
        try:
            parser.parse(tokens)
            print("✔️ Sentença aceita!")
        except Exception as e:
            print(f"❌ Erro detectado: {e}")

if __name__ == "__main__":
    main()