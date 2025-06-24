import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from SLR import SLRParser

# Produções da gramática:
producoes = [
    {'cabeca': "S'", 'corpo': ['E']},      # Produção 0
    {'cabeca': 'E', 'corpo': ['E', '*', 'n']},  # Produção 1
    {'cabeca': 'E', 'corpo': ['n']}        # Produção 2
]

# Coleção canônica de itens LR(0):
colecao_canonica = [
    # I0
    [
        {'cabeca': "S'", 'corpo': ['E'], 'ponto': 0},
        {'cabeca': 'E', 'corpo': ['E', '*', 'n'], 'ponto': 0},
        {'cabeca': 'E', 'corpo': ['n'], 'ponto': 0}
    ],
    # I1 (GOTO(0, E))
    [
        {'cabeca': "S'", 'corpo': ['E'], 'ponto': 1},
        {'cabeca': 'E', 'corpo': ['E', '*', 'n'], 'ponto': 1}
    ],
    # I2 (SHIFT em 'n' a partir de I0)
    [
        {'cabeca': 'E', 'corpo': ['n'], 'ponto': 1}
    ],
    # I3 (SHIFT em '*' a partir de I1)
    [
        {'cabeca': 'E', 'corpo': ['E', '*', 'n'], 'ponto': 2}
    ],
    # I4 (SHIFT em 'n' a partir de I3)
    [
        {'cabeca': 'E', 'corpo': ['E', '*', 'n'], 'ponto': 3}
    ],
    # I5 (Estado final, após GOTO(1, E) ou GOTO(3, E) se expandisse mais)
    [
        # Nenhum item válido com ponto à esquerda — estado de erro
    ]
]


# Conjunto FOLLOW:
follow = {
    "S'": {'$'},
    'E': {'$', '*'}
}

# Mock da gramática:
gramatica = type('G', (), {'producoes': producoes})()

# Instanciando o parser:
parser = SLRParser(gramatica, colecao_canonica, follow)

testes = [
    (['b', 'a'], "Válido: b a"),
    (['b'], "Inválido: falta o a"),
    (['a', 'b'], "Inválido: ordem invertida"),
    (['b', 'b', 'a'], "Inválido: b b a"),
    (['b', 'a', 'a'], "Inválido: b a a"),
    ([], "Inválido: vazio"),
    (['c', 'a'], "Inválido: símbolo desconhecido"),
    (['b', 'a', 'b', 'a'], "Inválido: duas sentenças coladas"),
]

# Rodando os testes:
for tokens, descricao in testes:
    print(f"\nTeste - {descricao}: Entrada: {tokens}")
    try:
        parser.parse(tokens)
        print("✔️ Sentença aceita!")
    except Exception as e:
        print(f"❌ Erro detectado: {e}")
