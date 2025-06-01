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
        ("a(ab)*", ["", "aab", "b", "bb", "ab", "ba", "aaaaaa"]),
    ]

    for er, testes in exemplos:
        print(f"\n=== Testando ER: '{er}' ===")
        exp = ExpressaoRegular(er)
        afd = exp.construir_afd()
        print("Estados finais do AFD:", [str(e) for e in afd.get_finais()])
        print("Transições do AFD:")
        for t in afd.get_transicoes():
            print(f"{t.get_origem()} --{t.get_simbolo()}--> {t.get_destino()}")
        for palavra in testes:
            print(f"Palavra: '{palavra}' - Aceita: {afd.aceita(palavra)}")

        exportar_afd(afd)
