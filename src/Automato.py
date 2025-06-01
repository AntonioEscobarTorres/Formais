from src.Estado import Estado
from src.Transicao import Transicao
from typing import Set
from collections import deque

class Automato:

    # Inicializa o autômato com número de estados, estado inicial, estados finais,
    # conjunto de transições e alfabeto.
    def __init__(self, n_estados: int, inicial : Estado, finais : set[Estado],
                 transicoes : set[Transicao] , alfabeto : set[str]):
        
        self.n_estados = n_estados
        self.inicial = inicial
        self.finais = finais
        self.transicoes = transicoes
        self.alfabeto = alfabeto

    # Calcula o ε-fecho de um estado, ou seja, o conjunto de estados 
    # alcançáveis apenas por transições ε ("&").
    def calcula_efecho(self , estadoInicial : Estado) -> set[Estado]:
        if estadoInicial is None:
            print("[WARN calcula_efecho] estadoInicial is None, returning empty set.")
            return set()

        # Inicializa o conjunto de estados visitados com o estado inicial
        # e uma pilha para fazer a busca em profundidade (DFS).
        visited = {estadoInicial} 
        stack = [estadoInicial]    

        # Enquanto houver estados a explorar na pilha:
        # remove o estado do topo da pilha,
        # percorre todas as transições do autômato,
        # se encontrar uma transição ε (representada por "&") a partir do estado atual,
        # e o estado destino ainda não tiver sido visitado,
        # adiciona-o ao conjunto de visitados e empilha para exploração futura.
        while stack:
            estadoAtualPilha = stack.pop()
            
            for transicao in self.transicoes:
                if transicao.get_origem() == estadoAtualPilha and transicao.get_simbolo() == "&":
                    if transicao.get_destino() not in visited:
                        visited.add(transicao.get_destino())
                        stack.append(transicao.get_destino())  
        # Retorna o conjunto de estados alcançáveis por 
        # transições ε a partir do estado inicial.
        return visited

    # Gera um nome único para um conjunto de
    # estados (útil para estados compostos do DFA).
    def gerar_nome(self, conjunto_estados: set[Estado]) -> str:
        if not conjunto_estados:
            return "ESTADO_VAZIO"

        state_names = []
        for estado in conjunto_estados:
            name = estado.get_estado()
            if not isinstance(name, str):
                print(f"[WARN gerar_nome] Non-string state name found: {name!r} from {estado!r}. Converting to str.")
                name = str(name)
            state_names.append(name)
        return ';'.join(sorted(state_names))

    # Verifica se algum estado no conjunto é um estado final do NFA.
    def contem_final(self, conjunto_nfa_estados: set[Estado]) -> bool:
        if not conjunto_nfa_estados:
            return False
        for nfa_estado_in_set in conjunto_nfa_estados:
            if nfa_estado_in_set in self.finais: 
                return True
        return False

    # Calcula os estados alcançáveis por um determinado símbolo a partir
    # de um conjunto de estados e retorna o ε-fecho desses destinos.
    def calcula_fecho_dos_destinos(self, conjunto_atual_nfa_estados: set[Estado], simbolo: str) -> set[Estado]:
        # Encontra todos os estados de destino que podem ser alcançados
        # diretamente a partir de qualquer estado do conjunto atual usando o símbolo fornecido.
        destinos_diretos = set()
        for estado_nfa in conjunto_atual_nfa_estados:
            for transicao in self.transicoes:
                if transicao.get_origem() == estado_nfa and transicao.get_simbolo() == simbolo:
                    destinos_diretos.add(transicao.get_destino())
        
        # Em seguida, para cada estado de destino direto encontrado, calcula seu ε-fecho
        # e adiciona todos os estados alcançáveis por ε-transições ao conjunto final de destinos.
        fecho_final_destinos = set()
        for destino_nfa in destinos_diretos:
            if destino_nfa is not None:
                 fecho_final_destinos.update(self.calcula_efecho(destino_nfa))

        # Retorna o conjunto de estados acessíveis a partir do conjunto atual,
        # por uma transição com o símbolo dado seguida de zero ou mais ε-transições.
        return fecho_final_destinos

    # Constrói um autômato determinístico (DFA) a partir do autômato atual (NFA).
    # Se token_map_afn for fornecido, associa os tokens aos estados finais do DFA.
    def determinizar(self, token_map_afn=None):

        # Caso o afd não tenha estado inicial
        if self.inicial is None:

            empty_dfa_initial = Estado("EMPTY_DFA_INITIAL")
            return Automato(0, empty_dfa_initial, set(), set(), self.alfabeto), {} if token_map_afn is not None else Automato(0, empty_dfa_initial, set(), set(), self.alfabeto)

        # 1. Calcula E-fecho do estado inicial do NFA
        estado_inicial_nfa_set = self.calcula_efecho(self.inicial)
        
        # Gera nome para o estado inicial do DFA
        nome_inicial_dfa = self.gerar_nome(estado_inicial_nfa_set)

        # Cria o primeiro estado do DFA (objeto Estado) e armazena
        dfa_estado_obj_inicial = Estado(nome_inicial_dfa)
        
        # Mapa de nomes de estados DFA para objetos Estado DFA
        map_nome_dfa_para_obj_estado_dfa = {nome_inicial_dfa: dfa_estado_obj_inicial}
        
        # Fila de conjuntos de estados NFA a serem processados (para criar estados DFA)
        fila_conjuntos_nfa = deque([estado_inicial_nfa_set]) 
        
        # Conjunto de nomes de estados finais do DFA
        nomes_finais_dfa = set()
        # Conjunto de transições do DFA
        transicoes_dfa = set()
        # Mapa de tokens para o DFA: nome do estado DFA (str) -> token (str)
        token_map_afd = {} if token_map_afn is not None else None
        
        conjuntos_nfa_processados_nomes = {nome_inicial_dfa}

        # Loop principal: construção dos estados e transições do AFD
        while fila_conjuntos_nfa:
            conjunto_nfa_atual = fila_conjuntos_nfa.popleft() 
            nome_dfa_atual = self.gerar_nome(conjunto_nfa_atual)

            # Se o conjunto atual contém algum estado final do NFA, o estado 
            # DFA correspondente também será final
            if self.contem_final(conjunto_nfa_atual):
                nomes_finais_dfa.add(nome_dfa_atual)
                
                # Mapeia o token correspondente ao primeiro estado final encontrado no conjunto (se houver)
                if token_map_afn is not None:
                    for estado_nfa_constituinte in sorted(list(conjunto_nfa_atual), key=lambda s: s.get_estado()):
                        nome_estado_nfa_constituinte = estado_nfa_constituinte.get_estado()
                        if nome_estado_nfa_constituinte in token_map_afn:
                            token_para_nfa = token_map_afn[nome_estado_nfa_constituinte]
                            token_map_afd[nome_dfa_atual] = token_para_nfa

                            break 
            
            # Para cada símbolo do alfabeto, calcula o próximo conjunto de estados NFA acessíveis
            for simbolo in sorted(list(self.alfabeto)): 
                
                proximo_conjunto_nfa = self.calcula_fecho_dos_destinos(conjunto_nfa_atual, simbolo)

                if proximo_conjunto_nfa: 
                    nome_proximo_dfa = self.gerar_nome(proximo_conjunto_nfa)

                    # Se esse conjunto ainda não foi processado, cria e enfileira novo estado DFA
                    if nome_proximo_dfa not in map_nome_dfa_para_obj_estado_dfa:
                        dfa_estado_obj_proximo = Estado(nome_proximo_dfa)
                        map_nome_dfa_para_obj_estado_dfa[nome_proximo_dfa] = dfa_estado_obj_proximo
                        
                        fila_conjuntos_nfa.append(proximo_conjunto_nfa)
                        conjuntos_nfa_processados_nomes.add(nome_proximo_dfa)                    
                    
                    # Adiciona a nova transição ao conjunto do DFA
                    origem_obj_dfa = map_nome_dfa_para_obj_estado_dfa[nome_dfa_atual]
                    destino_obj_dfa = map_nome_dfa_para_obj_estado_dfa[nome_proximo_dfa]
                    nova_transicao_dfa = Transicao(origem_obj_dfa, simbolo, destino_obj_dfa)
                    transicoes_dfa.add(nova_transicao_dfa)

        # A partir daqui, montagem final do AFD a partir das estruturas criadas
        finais_obj_dfa = {map_nome_dfa_para_obj_estado_dfa[nome] for nome in nomes_finais_dfa}
        afd = Automato(
            len(map_nome_dfa_para_obj_estado_dfa),
            map_nome_dfa_para_obj_estado_dfa[nome_inicial_dfa], 
            finais_obj_dfa,                                   
            transicoes_dfa,
            self.alfabeto
        )

        # Retorna o AFD e, se aplicável, o mapeamento de tokens
        if token_map_afd is not None:
            return afd, token_map_afd
        return afd

    def __str__(self):
        inicial_str = "None" if self.inicial is None else self.inicial.get_estado()
        
        finais_str = '; '.join(sorted(str(estado.get_estado()) for estado in self.finais))
        sorted_transicoes = sorted(
            list(self.transicoes), 
            key=lambda t: (
                t.get_origem().get_estado() if t.get_origem() else "",
                t.get_simbolo(), 
                t.get_destino().get_estado() if t.get_destino() else ""
            )
        )
        transicoes_str = '\n'.join(f'{str(transicao)}' for transicao in sorted_transicoes)
        alfabeto_str = ', '.join(sorted(self.alfabeto))

        return (
            f"{self.get_numero_de_estados()}\n"
            f"{inicial_str}\n"
            f"{finais_str}\n"
            f"{alfabeto_str}\n"
            f"{transicoes_str}\n"
        )

    # Retorna o conjunto de todos os estados usados no autômato.
    def get_estados(self) -> Set[Estado]:
        estados = set()
        if self.inicial: 
            estados.add(self.inicial)
        estados.update(self.finais)
        for transicao in self.transicoes:
            if transicao.get_origem():
                 estados.add(transicao.get_origem())
            if transicao.get_destino():
                 estados.add(transicao.get_destino())
        return estados

    def get_numero_de_estados(self) -> int:
        conjunto_de_estados = self.get_estados()
        return len(conjunto_de_estados)

    def get_transicoes(self):
        return self.transicoes

    def get_inicial(self):
        return self.inicial

    def get_finais(self):
        return self.finais

    def get_alfabeto(self):
        return self.alfabeto
    
    def aceita(self, palavra: str) -> bool:
        estado_atual = self.inicial
        for simbolo in palavra:
            transicoes = [t for t in self.transicoes if t.get_origem() == estado_atual and t.get_simbolo() == simbolo]
            if not transicoes:
                return False
            estado_atual = transicoes[0].get_destino()
        return estado_atual in self.finais