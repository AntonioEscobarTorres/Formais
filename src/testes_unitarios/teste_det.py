from src.Estado import Estado
from src.Transicao import Transicao
from src.Automato import Automato

# Estados
q0 = Estado("q0")
q1 = Estado("q1")
q2 = Estado("q2")

# Transições
t1 = Transicao(q0, 'a', q0)
t2 = Transicao(q0, 'a', q1)
t3 = Transicao(q0, 'b', q0)

t4 = Transicao(q1, 'a', q2)

t5 = Transicao(q2, 'a', q2)
t6 = Transicao(q2, 'b', q2)

# Criando o autômato
A = Automato(
    n_estados=3,
    inicial=q0,
    finais={q2},
    transicoes={t1,t2, t3, t4, t5, t6},
    alfabeto={'a', 'b'})

print(A.calcula_efecho(q0))
print(A.determinizar())


