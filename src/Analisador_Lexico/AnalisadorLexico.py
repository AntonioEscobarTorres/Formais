import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Analisador_Lexico.Estado import Estado
from Analisador_Lexico.Transicao import Transicao
from Analisador_Lexico.Automato import Automato
from Analisador_Lexico.ExpressaoRegular import ExpressaoRegular
from Analisador_Lexico.LeitorDeEr import LeitorDeEr

class AnalisadorLexico:
  
    def __init__(self, caminho_expressoes="./Testes/expressoes1.txt", caminho_entrada="./Testes/palavras_reservadas.txt"):
        
        # Lê expressões regulares com seus respectivos tokens e prioridades a partir de um arquivo
        self.expressoes = LeitorDeEr.ler_arquivo_er(caminho_expressoes)
        self.token_map = {}  # estado final → token
        self.afn_unificado = None
        self.afd = None

        # Processa todas as expressões para gerar o autômato final
        self._processar()

        # Associa cada palavra lida ao seu token correspondente
        self.tabela_de_simbolos = {} # Palavra lida -> Padrão 
        self.analisar_entrada(LeitorDeEr.ler_arquivo_entrada(caminho_entrada))
    
    # Analisa uma lista de palavras e retorna uma lista com seus respectivos tokens reconhecidos
    def analisar_entrada(self, entrada: list[str]) -> list[tuple[str, str]]:
        resultado = []

        for palavra in entrada:
            token = self.reconhecer_token(palavra)
            resultado.append((palavra, token))

        return resultado

    def _processar(self):
        # Processa todas as expressões regulares e constrói o AFD final
        automatos = []
        
        nfa_original_final_state_info = {}
        for priority, token, er in self.expressoes:
            afn = ExpressaoRegular(er).construir_afd()
            afn_index = len(automatos)
            for estado_final_nfa in afn.get_finais():
                nfa_state_name = f"T{afn_index}_{estado_final_nfa.get_estado()}"
                if nfa_state_name not in nfa_original_final_state_info or \
                   priority < nfa_original_final_state_info[nfa_state_name][1]:
                    nfa_original_final_state_info[nfa_state_name] = (token, priority)
            automatos.append((token, afn))

        # Cria um AFN unificado pela união via transição-ε
        self.afn_unificado = self.uniao_via_etransicao(automatos)
        
        # Prepara o mapeamento de estados finais para tokens, removendo a prioridade    
        temp_nfa_map_for_determinize = {
            state: info[0] for state, info in nfa_original_final_state_info.items()
        }
        
        # Determiniza o AFN unificado e obtém o AFD e uma tabela parcial de tokens
        self.afd, tabela_de_tokens_do_determinizar = self.afn_unificado.determinizar(temp_nfa_map_for_determinize) 
        print("------------------------------")
        print("Tabela de tokens (determinizada):")
        print(f"{tabela_de_tokens_do_determinizar}")

        final_prioritized_afd_token_map = {}
        
        # Resolve conflitos de estados finais no AFD usando a menor prioridade como critério
        for afd_final_state_obj in self.afd.get_finais():
            afd_state_name_str = afd_final_state_obj.get_estado()
            component_unified_nfa_state_names = afd_state_name_str.split(';')
            best_token_for_afd_state = None
            highest_priority_value = float('inf')
            for unified_nfa_name_component in component_unified_nfa_state_names:
                unified_nfa_name_component = unified_nfa_name_component.strip()
                if unified_nfa_name_component in nfa_original_final_state_info:
                    token_candidate, priority_candidate = nfa_original_final_state_info[unified_nfa_name_component]
                    if priority_candidate < highest_priority_value:
                        highest_priority_value = priority_candidate
                        best_token_for_afd_state = token_candidate
            if best_token_for_afd_state is not None:
                final_prioritized_afd_token_map[afd_state_name_str] = best_token_for_afd_state
        self.token_map = final_prioritized_afd_token_map

    def reconhecer_token(self, palavra: str) -> str:
        # Simula a leitura da palavra no AFD para encontrar o token correspondente
        estado_atual = self.afd.get_inicial()
        #print(f"[DEBUG] Estado inicial: {estado_atual.estado}")

        for simbolo in palavra:
            #print(f"[DEBUG] Lendo símbolo: {simbolo}")
            transicoes = [t for t in self.afd.get_transicoes()
                        if t.get_origem() == estado_atual and t.get_simbolo() == simbolo]
            if not transicoes:
                #print("[DEBUG] Nenhuma transição encontrada")
                return "Token não reconhecido"
            estado_atual = transicoes[0].get_destino()
            #print(f"[DEBUG] Novo estado: {estado_atual.estado}")

        if estado_atual in self.afd.get_finais():

            self.tabela_de_simbolos[palavra] = self.token_map.get(estado_atual.estado, "Token desconhecido")

            return self.token_map.get(estado_atual.estado, "Token desconhecido")
            
        return "Token não reconhecido"


    def uniao_via_etransicao(self, automatos: list[Automato]):
        # Realiza a união dos AFNs via transição-ε, renomeando estados para evitar conflitos
        novo_estado_inicial = Estado("inicial")
        todos_estados = {novo_estado_inicial}
        todas_transicoes = set()
        estados_finais = set()
        alfabeto_total = set()

        for i, (token, afn) in enumerate(automatos):
            prefixo = f"T{i}"
            # Renomeia os estados do AFN para garantir unicidade
            estados_renomeados = {
                estado: Estado(f"{prefixo}_{estado}") for estado in afn.get_estados()
            }
            todos_estados.update(estados_renomeados.values())
            for transicao in afn.get_transicoes():
                origem = estados_renomeados[transicao.get_origem()]
                destino = estados_renomeados[transicao.get_destino()]
                simbolo = transicao.get_simbolo()
                todas_transicoes.add(Transicao(origem, simbolo, destino))
            # Conecta o novo estado inicial à inicial do AFN via ε
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
        # Imprime a tabela de símbolos gerada após a análise léxica
        for lexema, token in self.tabela_de_simbolos.items():
            print(f"<{lexema},{token}>")

    def get_automato_afn(self) -> Automato:
        return self.afn_unificado

    def get_automato_afd(self) -> Automato:
        return self.afd

    def salvar_AFD(self, nome_arquivo="./arquivos_gerados/afd_salvo.txt"):
        if self.afd is None:
            print("Erro: O AFD não foi gerado ou é None. Nada para salvar.")
            return
        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
                arquivo.write(str(self.afd))
            print(f"AFD salvo com sucesso no arquivo '{nome_arquivo}'")

        except Exception as e:
            print(f"Ocorreu um erro ao tentar salvar o AFD no arquivo: {e}")

    def salvar_tabela_de_simbolos(self, nome_arquivo="./arquivos_gerados/tabela_de_simbolos.txt"):
        if not self.tabela_de_simbolos.items:
            print(f"Aviso: Tabela de símbolos está vazia. O arquivo '{nome_arquivo}' será criado vazio ou não será modificado se já existir vazio.")
            try:
                with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
                    pass
                print(f"Arquivo '{nome_arquivo}' preparado (tabela de símbolos vazia).")
            except Exception as e:
                print(f"Ocorreu um erro ao tentar criar/truncar o arquivo '{nome_arquivo}': {e}")
            return

        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
                for lexema, token in self.tabela_de_simbolos.items():
                    arquivo.write(f"<{lexema},{token}>\n")
            print(f"Tabela de símbolos salva com sucesso no arquivo '{nome_arquivo}'")

        except Exception as e:
            print(f"Ocorreu um erro ao tentar salvar a tabela de símbolos no arquivo: {e}")

    def __str__(self):
        return str(self.afd)