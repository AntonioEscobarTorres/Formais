from Estado import Estado
from Transicao import Transicao
from Automato import Automato
from ExpressaoRegular import ExpressaoRegular

class AnalisadorLexico:
  
    def __init__(self, expressoes: list[tuple[str, str]]):  # (token, regex)
        self.expressoes = expressoes
        self.token_map = {}  # estado final → token
        self.afn_unificado = None
        self.afd = None
        self._processar()


    def _processar(self):
        automatos = []
        self.token_map = {}  # Certifique-se de inicializar aqui também

        for token, er in self.expressoes:
            afn = ExpressaoRegular(er).thompson()
            print(afn)

            
            for estado_final in afn.get_finais():
                self.token_map[estado_final.get_estado()] = token



            automatos.append((token, afn))

        self.afn_unificado = self.uniao_via_etransicao(automatos)

        self.afd, tabela_tokens_atualizada = self.afn_unificado.determinizar(self.token_map)
     
        for token in tabela_tokens_atualizada.keys():
            self.token_map[token] = tabela_tokens_atualizada[token]
       
        
        # ✅ Passo 2: construir mapeamento do token nos estados finais do AFD
        for estado in self.afd.get_finais():
            nomes_estados_afn = estado.estado.split(',')
            for nome_afn in nomes_estados_afn:
                if nome_afn in self.token_map:
                    self.token_map[estado.estado] = self.token_map[nome_afn]
                    break

        print(self.token_map)


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
            return self.token_map.get(estado_atual.estado, "Token desconhecido")

        print("[DEBUG] Estado final não alcançado")
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


    def get_automato_afn(self) -> Automato:
        return self.afn_unificado

    def get_automato_afd(self) -> Automato:
        return self.afd

    def __str__(self):
        return str(self.afd)
