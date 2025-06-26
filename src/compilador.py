import re
import sys
import os
from Analisador_Sintatico.AnalisadorSintatico import AnalisadorSintatico
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Compilador:
    """
    Classe principal que orquestra as etapas de compilação:
    1. Carrega uma tabela de símbolos pré-definida de um arquivo.
    2. Processa o código-fonte linha por linha.
    3. Para cada linha, converte os lexemas em tipos de token baseados na tabela.
    4. Envia a lista de tipos de token de cada linha para o Analisador Sintático.
    """
    def __init__(self, codigo_path, tabela_simbolos_path):
        self.codigo_path = codigo_path
        self.tabela_simbolos_path = tabela_simbolos_path
        
        # O dicionário que armazenará a tabela de símbolos pré-definida.
        # Mapeia um lexema (palavra) para seu tipo de token (ex: 'var' -> 'var', 'contador' -> 'id')
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

    def compilar(self):

        self.carregar_tabela_de_simbolos()

        analisador = AnalisadorSintatico("./Testes/gramatica_completa.txt")
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
            if not linha_strip:
                continue
            
            lexemas_da_linha = linha_strip.split()
            
            for lexema in lexemas_da_linha:
                print(lexema)
                tipo_token = self.tabela_de_simbolos.get(lexema)
                print(tipo_token)
                if tipo_token:
                    tokens_para_parser.append(tipo_token)
                else:
                    tokens_para_parser.append(lexema)

        print(f"  Tokens da linha convertidos para: {tokens_para_parser}")
        analisador.analisar(tokens_para_parser)
        
        print("-" * 50)
        print("\nCompilação finalizada.")