from Estado import Estado
from Transicao import Transicao
from Automato import Automato


#_______________________________#
# Test união por e-transição

# Estados do autômato B
p0 = Estado("q0")
p1 = Estado("q1")

# Transições do autômato B
s1 = Transicao(p0, 'b', p1)
s2 = Transicao(p1, 'b', p1)

# Autômato B
B_plus = Automato(
    n_estados=2,
    inicial=p0,
    finais={p1},
    transicoes={s1, s2},
    alfabeto={'b'}
)

# Estados
s0 = Estado("q2")  # Estado inicial (não final)
s1 = Estado("q3")  # Estado final

# Transições
t1 = Transicao(s0, 'a', s1)  # Primeira ocorrência de 'a'
t2 = Transicao(s1, 'a', s1)  # Repete 'a' quantas vezes quiser

# Autômato A+
A_plus = Automato(
    n_estados=2,
    inicial=s0,
    finais={s1},
    transicoes={t1, t2},
    alfabeto={'a'}
)



def uniao_via_etransicao(automatos = list[Automato]):

    novo_estado_inicial = Estado("inicial")

    todos_estados = {novo_estado_inicial}
    todas_transicoes = set()
    estados_finais = set()
    alfabeto_total = set()

    for i, automato in enumerate(automatos):
        prefixo = f"A{i}"

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


automatos_teste_uniao = [A_plus, B_plus]
automato_unido = uniao_via_etransicao(automatos_teste_uniao)
print(automato_unido)
print(automato_unido.determinizar())