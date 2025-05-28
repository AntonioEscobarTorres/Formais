from Estado import Estado
from Transicao import Transicao
from Automato import Automato
from ExpressaoRegular import ExpressaoRegular

class AnalisadorLexico:
    def __init__(self, expressoes: list[str]):
        self.expressoes = expressoes
        self.afn_unificado = None
        self.afd = None
        self._processar()

    def _processar(self):
        automatos = []
        for er in self.expressoes:
            afn = ExpressaoRegular(er).thompson()
            automatos.append(afn)

        self.afn_unificado = self.uniao_via_etransicao(automatos)
        self.afd = self.afn_unificado.determinizar()


    def uniao_via_etransicao(self, automatos = list[Automato]):

        novo_estado_inicial = Estado("inicial")

        todos_estados = {novo_estado_inicial}
        todas_transicoes = set()
        estados_finais = set()
        alfabeto_total = set()

        for i, automato in enumerate(automatos):
            prefixo = f"A{i}"
            print(automato)
            # Renomeia os estados para identificar de qual automato cada estado está vindo
            estados_renomeados = {
                estado: Estado(f"{prefixo}_{estado}") for estado in automato.get_estados()
            }


            # Adiciona os estados renomeados
            todos_estados.update(estados_renomeados.values())

            # Renomeia e adiciona as transições
            for transicao in automato.get_transicoes():
                origem = estados_renomeados[transicao.get_origem()]
                destino = estados_renomeados[transicao.get_destino()]
                simbolo = transicao.get_simbolo()
                todas_transicoes.add(Transicao(origem, simbolo, destino))

            # Transição ε do novo estado inicial para o estado inicial do autômato atual
            transicao_epsilon = Transicao(novo_estado_inicial, '&', estados_renomeados[automato.get_inicial()])
            todas_transicoes.add(transicao_epsilon)

            # Adiciona os estados finais renomeados
            estados_finais.update(estados_renomeados[estado] for estado in automato.get_finais())

            # Junta o alfabeto (sem incluir o ε)
            alfabeto_total.update(automato.get_alfabeto())

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
