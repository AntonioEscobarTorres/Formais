from ExpressaoRegular import ExpressaoRegular


def exportar_afd(afd, arquivo=None):
    estados = list(afd.get_estados())
    estados_idx = {estado: idx for idx, estado in enumerate(estados)}
    finais = [str(estados_idx[e]) for e in afd.get_finais()]
    inicial = estados_idx[afd.get_inicial()]
    alfabeto = sorted(afd.get_alfabeto())
    transicoes = []
    for t in afd.get_transicoes():
        origem = estados_idx[t.get_origem()]
        destino = estados_idx[t.get_destino()]
        simbolo = t.get_simbolo()
        transicoes.append(f"{origem},{simbolo},{destino}")
    linhas = [
        str(len(estados)),
        str(inicial),
        ",".join(finais),
        ",".join(alfabeto),
        *transicoes
    ]
    saida = "\n".join(linhas)
    print(saida)

if __name__ == "__main__":
    exemplos = [
        # (Expressão regular, [palavras de teste])
        ("a|b*", ["", "a", "b", "bb", "ab", "ba", "aaa"]),
        ("ab*", ["a", "ab", "abb", "b", "", "ba", "aab"]),
        ("(a|b)c", ["ac", "bc", "cc", "abc", "c", "a", "b"]),
        ("(a|b)*abb", ["abb", "aabb", "babb", "ababb", "ab", "aab", "bba"]),
        ("a*b*", ["", "a", "b", "aa", "bb", "ab", "ba", "aabbb"]),
        ("(ab)*", ["", "ab", "abab", "a", "b", "aba", "abb"]),
    ]

    for er, testes in exemplos:
        print(f"\n=== Testando ER: '{er}' ===")
        exp = ExpressaoRegular(er)
        afd = exp.construir_afd()

        exportar_afd(afd)
