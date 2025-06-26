import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Analisador_Sintatico.AnalisadorSintatico import AnalisadorSintatico

def main():

    analisador = AnalisadorSintatico("./Testes/gramatica.txt")

    print(f"Palavras reservadas encontradas: {analisador.get_palavras_reservadas()}")

    analisador.salvar_tabela_de_analise()

    casos_de_teste = [
        # --- Sentenças Válidas ---
        (['inicio', 'fim', '.'], "Válido: O programa mais simples possível."),
        (['var', 'id', ':', 'inteiro', ';', 'inicio', 'id', ':=', 'num_int', 'fim', '.'], "Válido: Declaração de variável e atribuição."),
        (['const', 'real', 'id', '=', 'num_real', ';', 'inicio', 'fim', '.'], "Válido: Declaração de constante."),
        (['inicio', 'se', 'verdadeiro', 'entao', 'leia', '(', 'id', ')', 'fim', '.'], "Válido: Estrutura 'se-entao' simples."),
        (['var', 'id', ':', 'booleano', ';', 'inicio', 'se', 'id', 'entao', 'id', ':=', 'falso', 'senao', 'id', ':=', 'verdadeiro', 'fim', '.'], "Válido: Estrutura 'se-entao-senao'."),
        (['var', 'id', ':', 'inteiro', ';', 'inicio', 'enquanto', 'id', '<', 'num_int', 'faca', 'id', ':=', 'id', '+', 'num_int', 'fim', '.'], "Válido: Laço 'enquanto' com expressão."),
        (['var', 'id', ':', 'inteiro', ';', 'inicio', 'repita', 'id', ':=', 'id', '-', 'num_int', 'ate', 'id', '=', 'num_int', 'fim', '.'], "Válido: Laço 'repita-ate'."),
        (['proc', 'id', ';', 'var', 'id', ':', 'inteiro', ';', 'inicio', 'id', ':=', 'num_int', 'fim', ';', 'inicio', 'fim', '.'], "Válido: Declaração de procedimento com corpo."),
        (['inicio', 'escreva', '(', 'id', ',', 'num_real', ',', 'literal', ')', 'fim', '.'], "Válido: 'escreva' com múltiplas expressões."),

        # --- Sentenças Inválidas ---
        (['inicio', 'fim'], "Inválido: Falta o ponto final '.' obrigatório."),
        (['var', 'id', ':', 'inteiro', ';', 'id', ':=', 'num_int', '.'], "Inválido: Comando de atribuição fora do bloco 'inicio'...'fim'."),
        (['var', 'id', ':', 'inteiro', ';', 'const', 'real', 'id', '=', 'num_int', ';', 'inicio', 'fim', '.'], "Inválido: Ordem de declaração incorreta (var antes de const)."),
        (['proc', 'id', ';', 'inicio', 'fim', ';', 'var', 'id', ':', 'inteiro', ';'], "Inválido: Ordem de declaração incorreta (procedimento antes de var)."),
        (['inicio', 'leia', '(', 'id', ')', 'escreva', '(', 'id', ')', 'fim', '.'], "Inválido: Falta o ponto e vírgula ';' entre os comandos."),
        (['inicio', 'se', 'verdadeiro', 'fim', '.'], "Inválido: Falta a palavra-chave 'entao' após a expressão do 'se'."),
        (['var', 'id', ',', 'id', 'inteiro', ';', 'inicio', 'fim', '.'], "Inválido: Falta o ':' na declaração de variável."),
        (['inicio', 'id', '=', 'num_int', 'fim', '.'], "Inválido: Operador de atribuição incorreto ('=' em vez de ':=')"),
        ([], "Inválido: Programa completamente vazio."),
    ]
    
    print("\n--- Iniciando Bateria de Testes Sintáticos ---")
    # 3. Itera sobre os casos de teste e executa a análise.
    for tokens, descricao in casos_de_teste:
        print("-" * 50)
        print(f"Caso de Teste: {descricao}")
        
        # O método analisar já imprime o resultado (aceito ou erro).
        analisador.analisar(tokens)

if __name__ == "__main__":
    main()