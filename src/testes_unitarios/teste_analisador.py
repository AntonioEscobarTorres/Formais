import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Analisador_Lexico.AnalisadorLexico import AnalisadorLexico

analisador = AnalisadorLexico()

print(30*"-")

analisador.print_tabela_de_simbolos()