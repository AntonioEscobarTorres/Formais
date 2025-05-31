from ExpressaoRegular import ExpressaoRegular

def simular_afd(afd, palavra):
    estado = afd.get_inicial()
    for simbolo in palavra:
        transicoes = [t for t in afd.get_transicoes() if t.get_origem() == estado and t.get_simbolo() == simbolo]
        if not transicoes:
            return False
        estado = transicoes[0].get_destino()
    return estado in afd.get_finais()

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
        print("Estados do AFD:")
        for estado in afd.get_estados():
            print(estado)
        print("Transições:")
        for t in afd.get_transicoes():
            print(f"{t.get_origem()} --{t.get_simbolo()}--> {t.get_destino()}")
        print("Estado inicial:", afd.get_inicial().get_estado())
        print("Estados finais:", [estado.get_estado() for estado in afd.get_finais()])

        for palavra in testes:
            resultado = simular_afd(afd, palavra)
            print(f"'{palavra}': {'ACEITA' if resultado else 'REJEITA'}")
