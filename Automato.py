from Estado import Estado
from Transicao import Transicao
from typing import Set
from collections import deque

class Automato:

    def __init__(self, n_estados: int, inicial : Estado, finais : set[Estado],
                 transicoes : set[Transicao] , alfabeto : set[str]):
        
        self.n_estados = n_estados
        self.inicial = inicial
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
                        stack.append(transicao. get_destino())  
                        
                                
        return visited



    def determinizar(self, token_map_afn):
        # Calcula E-fecho e define o estado inicial com um nome único
        estado_inicial_afd = self.calcula_efecho(self.inicial)
        nome_inicial = self.gerar_nome(estado_inicial_afd)
        

        # Cria o primeiro estado determinístico e o coloca na fila
        estados_deterministicos = {nome_inicial: Estado(nome_inicial)}
        fila = deque([estado_inicial_afd])

        finais_deterministicos = set()
        transicoes_deterministicas = set()
        token_map_afd = {} if token_map_afn is not None else None
        # Processa todos os conjuntos de estados
        while fila:
            conjunto_atual = fila.popleft()
            nome_atual = self.gerar_nome(conjunto_atual)

            if self.contem_final(conjunto_atual):

                finais_deterministicos.add(nome_atual)

                
                # Mapeia para o token, se desejado
                if token_map_afn is not None:
                    for estado in conjunto_atual:
                        if estado.estado in token_map_afn:
                            token_map_afd[nome_atual] = token_map_afn[estado.estado]
                            
                            break  # prioriza o primeiro token encontrado

            for simbolo in self.alfabeto:
                fecho_proximos = self.calcula_fecho_dos_destinos(conjunto_atual, simbolo)

                if fecho_proximos:
                    nome_proximo = self.gerar_nome(fecho_proximos)
                    if nome_proximo not in estados_deterministicos:
                        estados_deterministicos[nome_proximo] = Estado(nome_proximo)
                        fila.append(fecho_proximos)

                    transicoes_deterministicas.add(
                        Transicao(estados_deterministicos[nome_atual], simbolo, estados_deterministicos[nome_proximo])
                    )

        finais_convertidos = {estados_deterministicos[nome] for nome in finais_deterministicos}

        afd = Automato(
            len(estados_deterministicos),
            estados_deterministicos[nome_inicial],
            finais_convertidos,
            transicoes_deterministicas,
            self.alfabeto
        )

 
        # Retorna também o mapeamento dos tokens, se aplicável
        if token_map_afd is not None:
            return afd, token_map_afd
        return afd



    def gerar_nome(self, conjunto_estados: set) -> str:
        return ','.join(sorted([estado.estado for estado in conjunto_estados]))


    # Verifica se o conjunto de estados tem algum elemento que é estado final,
    # assim dando a condição de estado final para o estado unido
    def contem_final(self, conjunto):
        return any(estado in self.finais for estado in conjunto)

    # Calculo o Efecho dos estados alcançados a partir de um símbolo
    def calcula_fecho_dos_destinos(self, conjunto_atual, simbolo):
        # adiciona em destinos todas as transições que saem de algum estado do automato 
        destinos = {
            transicao.get_destino()
            for estado in conjunto_atual
            for transicao in self.transicoes
            if transicao.get_origem() == estado and transicao.get_simbolo() == simbolo
        }
        # Calcula o fecho dos destinos, para garantir que a transição fique correta
        fecho = set()
        for estado in destinos:
            fecho.update(self.calcula_efecho(estado))
        return fecho




    def __str__(self):
        # Formata os dados para impressão
        finais_str = ', '.join(str(estado) for estado in self.finais)
        transicoes_str = '\n'.join(f'  {str(transicao)}' for transicao in self.transicoes)
        alfabeto_str = ', '.join(sorted(self.alfabeto))

        return (
            "\n=== AUTÔMATO ===\n"
            f"Estado Inicial: {{{self.inicial}}}\n"
            f"Estados Finais: {{ {finais_str} }}\n"
            f"Alfabeto: {{{alfabeto_str}}}\n"
            "Transições:\n"
            f"{transicoes_str}\n"
            "=================\n"
    )

    def get_estados(self) -> Set[Estado]:
        estados = set()

        # Adiciona o estado inicial
        estados.add(self.inicial)

        # Adiciona os estados finais
        estados.update(self.finais)

        # Adiciona todos os estados que aparecem nas transições
        for transicao in self.transicoes:
            estados.add(transicao.get_origem())
            estados.add(transicao.get_destino())

        return estados

    def get_transicoes(self):
        return self.transicoes

    def get_inicial(self):
        return self.inicial

    def get_finais(self):
        return self.finais

    def get_alfabeto(self):
        return self.alfabeto

