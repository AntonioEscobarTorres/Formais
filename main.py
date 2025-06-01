from src.AnalisadorLexico import AnalisadorLexico

analisador = AnalisadorLexico()

print(30*"-")

analisador.salvar_AFD()
print("")
analisador.salvar_tabela_de_simbolos()