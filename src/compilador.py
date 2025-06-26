import re
import sys
import os
from Analisador_Sintatico.AnalisadorSintatico import AnalisadorSintatico
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Compilador:
    def __init__(self, codigo_path, tabela_simbolos_path, palavras_reservadas_path):
        self.codigo_path = codigo_path
        self.tabela_simbolos_path = tabela_simbolos_path
        self.palavras_reservadas_path = palavras_reservadas_path

        self.tabela_simbolos = []
        self.palavras_reservadas = set()
        self.index_simbolos = {}  # mapeia lexema → (posição, categoria)

        self.tokens = []

    def salvar_tabela_simbolos(self):
        with open(self.tabela_simbolos_path, "w", encoding="utf-8") as f:
            for lexema, categoria in self.tabela_simbolos:
                f.write(f"<{lexema},{categoria}>\n")

    def analisar_lexico(self, codigo):
        with open("./Testes/tabela_de_simbolos_salvo.txt", "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if linha.startswith("<") and linha.endswith(">"):
                    conteudo = linha[1:-1]
                    if ',' in conteudo:
                        lexema, categoria = map(str.strip, conteudo.split(",", 1))
                        idx = len(self.tabela_simbolos)
                        self.tabela_simbolos.append((lexema, categoria))
                        self.index_simbolos[lexema] = (idx, categoria)
        # (2) Tokeniza o código-fonte (simples)
        lexemas = re.findall(r"[a-zA-Z_]\w*|[0-9]+(?:\.[0-9]+)?|:=|[^\s]", codigo)

        # (3) Monta a lista de tokens
        for lexema in lexemas:
            if lexema in self.palavras_reservadas:
                self.tokens.append((lexema, "PR"))  # Palavra reservada
            elif lexema in self.index_simbolos:
                pos, _ = self.index_simbolos[lexema]
                self.tokens.append(("id", pos))
            else:
                pos = len(self.tabela_simbolos)
                self.tabela_simbolos.append((lexema, "id"))
                self.index_simbolos[lexema] = (pos, "id")
                self.tokens.append(("id", pos))

        print(self.tabela_simbolos)
    def compilar(self):

        # Leitura do código-fonte
        with open(self.codigo_path, "r", encoding="utf-8") as f:
            codigo = f.read()

        self.analisar_lexico(codigo)

        # Chama o analisador sintático
        analisador = AnalisadorSintatico("./Testes/gramatica_completa.txt")
        analisador.salvar_tabela_de_analise()
        for tokens in self.tokens:
            analisador.analisar(tuple(self.tokens))

        # Salva possíveis novos identificadores na tabela
        self.salvar_tabela_simbolos()

if __name__ == "__main__":
    compilador = Compilador(
        codigo_path="./Testes/codigo_fonte.txt",
        tabela_simbolos_path="./Testes/tabela_de_simbolos_salvo.txt",
        palavras_reservadas_path="./Testes/palavras_reservadas1.txt"
    )
    compilador.compilar()