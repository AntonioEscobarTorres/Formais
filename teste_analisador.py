from AnalisadorLexico import AnalisadorLexico

# Lista de expressões regulares
expressoes = ["a*", "ab"]

# Instancia o analisador léxico com as ERs
analisador = AnalisadorLexico(expressoes)

# Imprime o AFD resultante da união e determinização
print(analisador.afd)
