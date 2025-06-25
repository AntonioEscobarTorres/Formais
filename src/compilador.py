import sys
import os
import re

# --- Documentação do Uso de IA Generativa ---
# Finalidade do uso: Refatoração da lógica da Tabela de Símbolos e do Analisador Léxico
# para produzir tokens formatados com metadados (índice na tabela), conforme nova especificação.
# Modelo utilizado: Gemini (por Google)
# Prompt(s) empregado(s):
# 1. "A atualização da tabela de símbolos agora deve ser alterada da seguinte forma: Se o
# lexema identificado já estiver na tabela de símbolos, deve-se retornar o tokens lá indicado...
# Caso contrário, o lexema deve ser incluído na tabela de símbolos e o lexema retornado deve ser
# do tipo <id, index>..."
# ------------------------------------------------

# Adiciona o diretório 'src' ao caminho do Python.
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.append(src_path)

from Analisador_Sintatico.AnalisadorSintatico import AnalisadorSintatico

class TabelaDeSimbolos:
    """
    Uma classe simples para gerir a tabela de símbolos.
    Armazena lexemas e o tipo de token associado.
    """
    def __init__(self):
        self.simbolos = {} # { 'lexema': (tipo_token, indice) }
        self.lista_ordenada = [] # [ {'lexema': ..., 'tipo': ...} ]

    def inserir_reservada(self, palavra):
        """Insere uma palavra reservada na tabela."""
        if palavra not in self.simbolos:
            indice = len(self.lista_ordenada)
            tipo_token = "palavra_reservada"
            self.simbolos[palavra] = (tipo_token, indice)
            self.lista_ordenada.append({'lexema': palavra, 'tipo': tipo_token})
    
    def procurar_ou_inserir_id(self, lexema):
        """
        Procura por um lexema e retorna o token para o parser e o token formatado.
        - Se for palavra reservada: retorna (lexema, <lexema, palavra_reservada>)
        - Se for ID (novo ou existente): retorna ('id', <id, indice>)
        """
        if lexema in self.simbolos:
            # Já existe (pode ser reservada ou um ID já visto)
            tipo_token, indice = self.simbolos[lexema]
            if tipo_token == "palavra_reservada":
                token_para_parser = lexema
                token_formatado = f"<{lexema}, palavra_reservada>"
            else: # É um ID já existente
                token_para_parser = "id"
                token_formatado = f"<id, {indice}>"
            return token_para_parser, token_formatado
        else:
            # É um novo ID. Insere na tabela.
            indice = len(self.lista_ordenada)
            tipo_token = "id"
            self.simbolos[lexema] = (tipo_token, indice)
            self.lista_ordenada.append({'lexema': lexema, 'tipo': tipo_token})
            token_para_parser = "id"
            token_formatado = f"<id, {indice}>"
            return token_para_parser, token_formatado

    def __str__(self):
        """Retorna uma representação em string da tabela."""
        linhas = ["--- Tabela de Símbolos ---"]
        for i, item in enumerate(self.lista_ordenada):
            linhas.append(f"Índice {i}: Lexema='{item['lexema']}', Tipo='{item['tipo']}'")
        return "\n".join(linhas)

def analise_lexica_simulada(codigo_fonte: str, tabela: TabelaDeSimbolos):
    """
    Simula a nova lógica do analisador léxico.
    Retorna duas listas: uma para o parser e uma formatada para visualização.
    """
    tokens_para_parser = []
    tokens_formatados = []
    # Regex para separar palavras, números, e operadores/pontuação.
    padrao = r'([a-zA-Z_]\w*)|(\d+\.\d+|\d+)|(<=|>=|<>|:=|\.\.|\.|\(|\)|\[|\]|[:;(),*=+<>/-])'
    
    for match in re.finditer(padrao, codigo_fonte):
        palavra, num, op = match.groups()
        
        if palavra:
            # Se for uma palavra, consulta a tabela de símbolos.
            token_parser, token_fmt = tabela.procurar_ou_inserir_id(palavra)
            tokens_para_parser.append(token_parser)
            tokens_formatados.append(token_fmt)
        elif num:
            # Simplificação: classifica números como tokens genéricos.
            token = "num_int" if '.' not in num else "num_real"
            tokens_para_parser.append(token)
            tokens_formatados.append(f"<{num}, {token}>")
        elif op:
            # Operadores e pontuação são seus próprios tokens.
            tokens_para_parser.append(op)
            tokens_formatados.append(f"<{op}, operador>")
            
    return tokens_para_parser, tokens_formatados


def main():
    # Caminhos para os ficheiros de entrada
    caminho_gramatica = "./Testes/gramatica_completa.txt"
    caminho_reservadas = "./Testes/palavras_reservadas.txt"
    caminho_codigo = "./Testes/codigo_fonte.txt"

    # Verifica se todos os ficheiros de entrada necessários existem antes de continuar.
    ficheiros_necessarios = [caminho_gramatica, caminho_reservadas, caminho_codigo]
    for ficheiro in ficheiros_necessarios:
        if not os.path.exists(ficheiro):
            print(f"ERRO CRÍTICO: O ficheiro de entrada '{ficheiro}' não foi encontrado.")
            print("Por favor, certifique-se de que a pasta 'Testes' existe na raiz do projeto e contém os ficheiros necessários.")
            sys.exit(1)

    # --- INTERFACE DE PROJETO ---
    print("--- INICIANDO INTERFACE DE PROJETO ---")

    # 1. Cria a tabela de símbolos e a pré-popula com palavras reservadas.
    tabela_de_simbolos = TabelaDeSimbolos()
    with open(caminho_reservadas, 'r') as f:
        for palavra in f:
            tabela_de_simbolos.inserir_reservada(palavra.strip())
    
    print("Tabela de símbolos pré-populada com palavras reservadas.")
    
    # 2. Constrói a tabela de análise a partir da gramática.
    print("\nConstruindo a tabela de análise a partir da gramática...")
    analisador_sintatico = AnalisadorSintatico(caminho_gramatica)
    analisador_sintatico.salvar_tabela_de_analise("tabela_slr_gerada.txt")
    print("--- FIM DA INTERFACE DE PROJETO ---\n")

    # --- INTERFACE DE EXECUÇÃO ---
    print("--- INICIANDO INTERFACE DE EXECUÇÃO ---")
    
    # 1. Lê o código fonte a ser analisado.
    with open(caminho_codigo, 'r') as f:
        codigo = f.read()
    
    print(f"Código Fonte a ser analisado:\n---\n{codigo}\n---")

    # 2. Executa a análise léxica simulada.
    tokens_para_parser, tokens_formatados = analise_lexica_simulada(codigo, tabela_de_simbolos)
    print(f"\nSaída do Analisador Léxico (Tokens Formatados): {tokens_formatados}")

    # 3. Executa a análise sintática.
    analisador_sintatico.analisar(tokens_para_parser)

    # 4. Imprime a tabela de símbolos final.
    print("\n" + str(tabela_de_simbolos))
    print("--- FIM DA INTERFACE DE EXECUÇÃO ---")


if __name__ == "__main__":
    main()
