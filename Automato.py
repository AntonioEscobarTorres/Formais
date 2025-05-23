from Estado import Estado
from Transicao import Transicao
from typing import Set
from collections import deque

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



    def determinizar(self):
        estado_inicial_afd = self.calcula_efecho(self.incial)
        nome_inicial = ''.join(sorted(estado.get_estado() for estado in estado_inicial_afd))
        estados_deterministicos = {nome_inicial: Estado(nome_inicial)}
        fila = deque([estado_inicial_afd])
        finais_deterministicos = set()
        transicoes_deterministicas = []

        while fila:
            conjunto_atual = fila.popleft()
            nome_atual = ''.join(sorted(estado.get_estado() for estado in conjunto_atual))
            
            if any(estado in self.finais for estado in conjunto_atual):
                finais_deterministicos.add(nome_atual)

            for simbolo in self.alfabeto:
                proximos_estados = set()
                for estado in conjunto_atual:
                    for transicao in self.transicoes:
                        if transicao.get_origem() == estado and transicao.get_simbolo() == simbolo:
                            proximos_estados.add(transicao.get_destino())
                fecho_proximos = set()
                for est in proximos_estados:
                    fecho_proximos.update(self.calcula_efecho(est))

                if fecho_proximos:
                    nome_proximo = ''.join(sorted(est.get_estado() for est in fecho_proximos))
                    if nome_proximo not in estados_deterministicos:
                        estados_deterministicos[nome_proximo] = Estado(nome_proximo)
                        fila.append(fecho_proximos)
                    transicoes_deterministicas.append(
                        Transicao(estados_deterministicos[nome_atual], simbolo, estados_deterministicos[nome_proximo])
                    )

        finais_convertidos = {estados_deterministicos[nome] for nome in finais_deterministicos}
        return Automato(len(estados_deterministicos), estados_deterministicos[nome_inicial], finais_convertidos, set(transicoes_deterministicas), self.alfabeto)



    def __str__(self):
        finais_str = ','.join(str(estado) for estado in self.finais)
        transicoes_str = '\n'.join(str(transicao) for transicao in self.transicoes)

        return (f'''"Estado Inicial: " {self.incial}
            "Estados Finais: " {finais_str}
            "Alfabeto: " {"{" + ','.join(self.alfabeto) + "}"}
            "Transições: "
            {transicoes_str}''')

