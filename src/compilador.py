import re
import sys
import os
from Analisador_Sintatico.AnalisadorSintatico import AnalisadorSintatico
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Compilador:

    def __init__(self, codigo_path, tabela_simbolos_path):
        self.codigo_path = codigo_path
        self.tabela_simbolos_path = tabela_simbolos_path
        self.tabela_de_simbolos = {}

    def carregar_tabela_de_simbolos(self):
        try:
            with open(self.tabela_simbolos_path, "r", encoding="utf-8") as f:
                for linha in f:
                    linha_temp = linha.strip()
                    linha_strip = linha_temp[1:-1]
                    if linha and ',' in linha_strip:
                        lexema, tipo = map(str.strip, linha_strip.split(",", 1))
                        self.tabela_de_simbolos[lexema] = tipo
            print(f"Tabela de símbolos carregada com sucesso de '{self.tabela_simbolos_path}'.")
        except FileNotFoundError:
            print(f"Erro: Arquivo da tabela de símbolos não encontrado em '{self.tabela_simbolos_path}'")
            sys.exit(1)

    def salvar_tabela_de_simbolos(self):
        try:
            with open('./arquivos_gerados/tabela_de_simbolos_atualizada.txt', "w", encoding="utf-8") as f:
                for lexema, tipo in self.tabela_de_simbolos.items():
                    f.write(f"<{lexema},{tipo}>\n")
            print(f"Tabela de símbolos atualizada foi salva em './arquivos_gerados/tabela_de_simbolos_atualizada.txt'.")
        except Exception as e:
            print(f"Erro ao salvar a tabela de símbolos: {e}")

    def compilar(self, path_gramatica="./Testes/gramatica_completa.txt"):

        self.carregar_tabela_de_simbolos()

        analisador = AnalisadorSintatico(path_gramatica)
        analisador.salvar_tabela_de_analise()

        try:
            with open(self.codigo_path, "r", encoding="utf-8") as f:
                codigo_linhas = f.readlines()
            print(f"Lendo código de '{self.codigo_path}' para análise linha a linha...")
        except FileNotFoundError:
            print(f"Erro: Arquivo de código-fonte não encontrado em '{self.codigo_path}'")
            sys.exit(1)
    
        tokens_para_parser = []
        for num_linha, linha in enumerate(codigo_linhas, 1):

            linha_strip = linha.strip()
            lexemas_da_linha = linha_strip.split()
            
            for lexema in lexemas_da_linha:

                tipo_token = self.tabela_de_simbolos.get(lexema)

                if tipo_token:
                    tokens_para_parser.append(tipo_token)

                elif lexema.isalpha():
                    print(f"  Novo identificador '{lexema}' detectado. Adicionando à tabela como <id,{len(self.tabela_de_simbolos)+1}>.")
                    self.tabela_de_simbolos[lexema] = 'id'
                    tokens_para_parser.append('id')
                else:
                    tokens_para_parser.append(lexema)

        #print(f"  Tokens da linha convertidos para: {tokens_para_parser}")
        analisador.analisar(tokens_para_parser)
        
        print("-" * 50)
        print("\nCompilação finalizada.")
        print("")
        self.salvar_tabela_de_simbolos()