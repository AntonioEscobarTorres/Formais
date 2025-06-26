from src.Analisador_Lexico.AnalisadorLexico import AnalisadorLexico
from src.compilador import Compilador
import sys

print("Escolha qual exemplo você deseja executar:")
print("1: Analisador Léxico (palavras_reservadas.txt)")
print("2: Analisador Sintático - Exemplo 1 (codigo_fonte.txt)")
print("3: Analisador Sintático - Exemplo 2 (codigo_fonte1.txt)")
print("4: Analisador Sintático - Exemplo 3 (codigo_fonte2.txt)")
print("5: Analisador Sintático - Exemplo 4 (codigo_fonte3.txt)")

escolha = input("Digite o número da sua escolha: ")

codigo_path = ""
tabela_simbolos_path = ""

if escolha == '1':
    print("\nExecutando: Analisador Léxico")
    codigo_path = "./Testes/palavras_reservadas.txt"
    expressoes_path="./Testes/expressoes1.txt"
elif escolha == '2':
    print("\nExecutando: Analisador Sintático - Exemplo 1")
    expressoes_path="./Testes/expressoes.txt"
    codigo_path = "./Testes/codigo_fonte.txt"
    tabela_simbolos_path = "./arquivos_gerados/tabela_de_simbolos.txt"
elif escolha == '3':
    print("\nExecutando: Analisador Sintático - Exemplo 2")
    expressoes_path="./Testes/expressoes.txt"
    codigo_path = "./Testes/codigo_fonte1.txt"
    tabela_simbolos_path = "./arquivos_gerados/tabela_de_simbolos.txt"
elif escolha == '4':
    print("\nExecutando: Analisador Sintático - Exemplo 3")
    expressoes_path="./Testes/expressoes.txt"
    codigo_path = "./Testes/codigo_fonte2.txt"
    tabela_simbolos_path = "./arquivos_gerados/tabela_de_simbolos.txt"
else:
    print("Escolha inválida. Saindo do programa.")
    sys.exit(1)

analisador = AnalisadorLexico(expressoes_path, codigo_path)

print(30*"-")
analisador.salvar_AFD()
print("")
analisador.salvar_tabela_de_simbolos()

if escolha in ['2','3','4'] :
    compilador = Compilador(
            codigo_path,
            tabela_simbolos_path
        )
    compilador.compilar()