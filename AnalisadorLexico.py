from Estado import Estado
from Transicao import Transicao
from Automato import Automato
from ExpressaoRegular import ExpressaoRegular
from LeitorDeEr import LeitorDeEr

class AnalisadorLexico:
  
    def __init__(self):  # (token, regex)
        self.expressoes = LeitorDeEr.ler_arquivo_er("./expressoes.txt")
        self.token_map = {}  # estado final → token
        self.afn_unificado = None
        self.afd = None
        self._processar()
        self.tabela_de_simbolos = {} # Palavra lida -> Padrão 
        self.analisar_entrada(LeitorDeEr.ler_arquivo_entrada("./testes.txt"))

    def analisar_entrada(self, entrada: list[str]) -> list[tuple[str, str]]:
        resultado = []

        for palavra in entrada:
            token = self.reconhecer_token(palavra)
            resultado.append((palavra, token))

        return resultado

    def ler_entrada(self):
        return "aaaaaa ab b baaaaab aaa ab acd"

    def ler_expressoes(self):
        return [
                ("NUM", "a*"),
                ("AB_TOKEN", "ab"),
                ("BnoINICIO", "b(a|b)*")
            ]

    def _processar(self):
        automatos = []
        
        nfa_original_final_state_info = {}
        print(self.expressoes)
        for priority, token, er in self.expressoes:
            afn = ExpressaoRegular(er).thompson()
            # print(f"AFN for {token} ({priority}): {afn}")

            for estado_final_nfa in afn.get_finais():
                nfa_state_name = estado_final_nfa.get_estado()
                if nfa_state_name not in nfa_original_final_state_info or \
                   priority < nfa_original_final_state_info[nfa_state_name][1]:
                    nfa_original_final_state_info[nfa_state_name] = (token, priority)
            
            automatos.append((token, afn))

        self.afn_unificado = self.uniao_via_etransicao(automatos)
        # print(f"AFN Unificado: {self.afn_unificado}")

        temp_nfa_map_for_determinize = {
            state: info[0] for state, info in nfa_original_final_state_info.items()
        }
        
        self.afd, tabela_de_tokens_do_determinizar = self.afn_unificado.determinizar(temp_nfa_map_for_determinize) 
        print(f"AFD: {self.afd}")
        print(f"Tabela de tokens (from determinizar): {tabela_de_tokens_do_determinizar}")

        final_prioritized_afd_token_map = {}
        
        #print(f"[DEBUG _processar] Nomes dos estados finais do AFD: {[s.get_estado() for s in self.afd.get_finais()]}")
        #print(f"[DEBUG _processar] Conteúdo de nfa_original_final_state_info: {nfa_original_final_state_info}")

        for afd_final_state_obj in self.afd.get_finais():
            afd_state_name_str = afd_final_state_obj.get_estado()
            #print(f"[DEBUG _processar] Processando estado final do AFD: {afd_state_name_str}")
            
            component_unified_nfa_state_names = afd_state_name_str.split(',')
            
            best_token_for_afd_state = None
            highest_priority_value = float('inf')

            for unified_nfa_name_component in component_unified_nfa_state_names:
                unified_nfa_name_component = unified_nfa_name_component.strip()
                
                original_nfa_name_candidate = unified_nfa_name_component

                if '_' in unified_nfa_name_component:
                    parts = unified_nfa_name_component.split('_', 1)
                    if len(parts) > 1 and parts[0].startswith('T') and parts[0][1:].isdigit():
                        original_nfa_name_candidate = parts[1]
                
                #print(f"[DEBUG _processar]   Componente unificado: {unified_nfa_name_component}, Candidato original: {original_nfa_name_candidate}")
                
                if original_nfa_name_candidate in nfa_original_final_state_info:
                    token_candidate, priority_candidate = nfa_original_final_state_info[original_nfa_name_candidate]
                    #print(f"[DEBUG _processar]     Encontrado em nfa_original_final_state_info: Token={token_candidate}, Prioridade={priority_candidate}")
                    
                    if priority_candidate < highest_priority_value:
                        highest_priority_value = priority_candidate
                        best_token_for_afd_state = token_candidate
                        #print(f"[DEBUG _processar]       Novo melhor token para {afd_state_name_str}: {best_token_for_afd_state} (Prioridade: {highest_priority_value})")

            if best_token_for_afd_state is not None:
                final_prioritized_afd_token_map[afd_state_name_str] = best_token_for_afd_state
                #print(f"[DEBUG _processar] Mapeado estado AFD '{afd_state_name_str}' para token '{best_token_for_afd_state}'")
            #else:
                #print(f"[DEBUG _processar] Nenhum token encontrado para o estado AFD '{afd_state_name_str}'")
        
        self.token_map = final_prioritized_afd_token_map
        #print(f"Token map final (prioritized): {self.token_map}") 

    def reconhecer_token(self, palavra: str) -> str:
        estado_atual = self.afd.get_inicial()
        print(f"[DEBUG] Estado inicial: {estado_atual.estado}")

        for simbolo in palavra:
            print(f"[DEBUG] Lendo símbolo: {simbolo}")
            transicoes = [t for t in self.afd.get_transicoes()
                        if t.get_origem() == estado_atual and t.get_simbolo() == simbolo]
            if not transicoes:
                print("[DEBUG] Nenhuma transição encontrada")
                return "Token não reconhecido"
            estado_atual = transicoes[0].get_destino()
            print(f"[DEBUG] Novo estado: {estado_atual.estado}")

        if estado_atual in self.afd.get_finais():

            print(f"[DEBUG] Estado final alcançado: {estado_atual.estado}")

            self.tabela_de_simbolos[palavra] = self.token_map.get(estado_atual.estado, "Token desconhecido")

            return self.token_map.get(estado_atual.estado, "Token desconhecido")
            
        return "Token não reconhecido"


    def uniao_via_etransicao(self, automatos: list[Automato]):
        novo_estado_inicial = Estado("inicial")
        todos_estados = {novo_estado_inicial}
        todas_transicoes = set()
        estados_finais = set()
        alfabeto_total = set()

        for i, (token, afn) in enumerate(automatos):
            prefixo = f"T{i}"
            estados_renomeados = {
                estado: Estado(f"{prefixo}_{estado}") for estado in afn.get_estados()
            }

            todos_estados.update(estados_renomeados.values())
            for transicao in afn.get_transicoes():
                origem = estados_renomeados[transicao.get_origem()]
                destino = estados_renomeados[transicao.get_destino()]
                simbolo = transicao.get_simbolo()
                todas_transicoes.add(Transicao(origem, simbolo, destino))

            todas_transicoes.add(
                Transicao(novo_estado_inicial, '&', estados_renomeados[afn.get_inicial()])
            )

            for estado_final in afn.get_finais():
                renomeado = estados_renomeados[estado_final]
                estados_finais.add(renomeado)
                self.token_map[renomeado.estado] = token  # associa estado → token

            alfabeto_total.update(afn.get_alfabeto())

        return Automato(
            len(todos_estados),
            novo_estado_inicial,
            estados_finais,
            todas_transicoes,
            alfabeto_total
        )


    def print_tabela_de_simbolos(self):
        for lexema, token in self.tabela_de_simbolos.items():
            print(f"<{lexema},{token}>")

    def get_automato_afn(self) -> Automato:
        return self.afn_unificado

    def get_automato_afd(self) -> Automato:
        return self.afd

    def __str__(self):
        return str(self.afd)
