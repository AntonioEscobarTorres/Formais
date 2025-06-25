import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Analisador_Sintatico.AnalisadorSintatico import AnalisadorSintatico

def main():

    analisador = AnalisadorSintatico("./testes/gramatica.txt")

    print(f"Palavras reservadas encontradas: {analisador.get_palavras_reservadas()}")

    analisador.salvar_tabela_de_analise()

    casos_de_teste = [
        # --- Sentenças Válidas ---
        (['inicio', 'fim', '.'], "Válido: Programa mínimo."),
        (['var', 'x', ',', 'y', ':', 'inteiro', ';', 'inicio', 'x', ':=', 'num_int', 'fim', '.'], "Válido: Declaração de variáveis e atribuição."),
        (['const', 'real', 'PI', '=', 'num_real', ';', 'inicio', 'fim', '.'], "Válido: Declaração de constante."),
        (['var', 'a', ':', 'booleano', ';', 'inicio', 'se', 'a', '=', 'verdadeiro', 'entao', 'escreva', '(', 'literal', ')', 'senao', 'escreva', '(', 'literal', ')', 'fim', '.'], "Válido: Estrutura condicional completa."),
        (['var', 'i', ':', 'inteiro', ';', 'inicio', 'enquanto', 'i', '<', 'num_int', 'faca', 'i', ':=', 'i', '+', 'num_int', 'fim', '.'], "Válido: Laço 'enquanto'."),
        (['proc', 'p', '(', 'val', 'a', ':', 'inteiro', ')', ';', 'inicio', 'fim', '.'], "Válido: Declaração de procedimento."),
        (['var', 'v', ':', 'vetor', '[', 'num_int', ']', 'de', 'real', ';', 'inicio', 'v', '[', 'num_int', ']', ':=', 'num_real', 'fim', '.'], "Válido: Uso de vetor."),

        # --- Sentenças Inválidas ---
        (['inicio', 'fim'], "Inválido: Falta do ponto final."),
        (['var', 'x', ':', 'inteiro', ';', 'x', ':=', 'num_int', '.'], "Inválido: Comando fora do bloco 'inicio'...'fim'."),
        (['var', 'i', ':', 'inteiro', ';', 'const', 'inteiro', 'MAX', '=', 'num_int', ';', 'inicio', 'fim', '.'], "Inválido: Ordem de declaração incorreta (var antes de const)."),
        (['inicio', 'leia', '(', 'x', ')', 'escreva', '(', 'x', ')', 'fim', '.'], "Inválido: Ponto e vírgula faltando entre comandos."),
        (['inicio', 'id', '=', 'num_int', 'fim', '.'], "Inválido: Operador de atribuição incorreto (= em vez de :=)."),
        (['inicio', 'se', 'a', '>', 'b', 'entao', 'fim', '.'], "Inválido: 'se' sem comando no corpo."),
        (['var', 'x', 'y', 'inteiro', ';', 'inicio', 'fim', '.'], "Inválido: Falta ':' na declaração de variável."),
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