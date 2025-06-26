from src.Analisador_Lexico.AnalisadorLexico import AnalisadorLexico
from src.compilador import Compilador

expressoes_path="./Testes/expressoes.txt"
codigo_path="./Testes/codigo_fonte1.txt"
tabela_simbolos_path="./Testes/tabela_de_simbolos_salvo.txt"

analisador = AnalisadorLexico(expressoes_path, codigo_path)

print(30*"-")
analisador.salvar_AFD()
print("")
analisador.salvar_tabela_de_simbolos()

compilador = Compilador(
        codigo_path,
        tabela_simbolos_path
    )
compilador.compilar()