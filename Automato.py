from Estado import Estado
from Transicao import Transicao
from typing import Set

class Automato:

    def __init__(self, n_estados: int, inicial : Estado, finais : set[Estado],
                 transicoes : set[Transicao] , alfabeto : set[str]):
        
        self.n_estados = n_estados
        self.incial = inicial
        self.finais = finais
        self.transicoes = transicoes
        self.alfabeto = alfabeto

        
    # Busca em profundidade para alcançar todos os estados alcançáveis por E do estado inicial. 
    def calcula_efecho(self , estadoInicial : Estado):
        visited = {estadoInicial}  # início do fecho
        stack = [estadoInicial]    # para visitar

        while stack:
            estadoAtualPilha = stack.pop()
            
            for transicao in self.transicoes:
                if transicao.get_origem() == estadoAtualPilha and transicao.get_simbolo() == "&":
                    if transicao.get_destino() not in visited:
                        visited.add(transicao.get_destino())
                        stack.append(transicao.get_destino())          
        return visited


    def __str__(self):
        estados_finais_str = ','.join(str(estado) for estado in self.__estados_finais)
        transicoes_str = '\n'.join(str(transicao) for transicao in self.__transicoes)

        return (f'''"Estado Inicial: " {self.__estado_inicial}
        "Estados Finais: " {estados_finais_str}
        "Alfabeto: " {"{" + ','.join(self.__alfabeto) + "}"}
        "Transicoes: "
        {transicoes_str}''')
