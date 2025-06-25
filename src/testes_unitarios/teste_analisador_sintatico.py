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
        (['b'], "Válido: Derivação mais simples (A -> E -> b)."),
        (['d'], "Válido: Derivação via B e C vazio (A -> B C -> d D -> d &)."),
        (['c', 'b'], "Válido: Recursão simples em E (A -> E -> c A -> c b)."),
        (['d', 'c'], "Válido: Derivação de C (A -> B C -> d (c D) -> d c &)."),
        (['c', 'c', 'b'], "Válido: Múltiplas recursões em E."),
        (['d', 'b', 'a'], "Válido: Derivação espelhada em D (A -> B C -> d D -> d (b D a) -> d b & a)."),
        (['a', 'd'], "Válido: Derivação de 'a' em B (A -> B C -> (a B) D -> a d &)."),

        # --- Sentenças Inválidas ---
        (['a'], "Inválido: 'a' deve ser seguido por 'd' (via B)."),
        (['c'], "Inválido: 'c' deve ser seguido por outra sentença (via A ou C)."),
        (['d', 'a'], "Inválido: 'a' após 'd' requer um 'b' intermediário."),
        (['a', 'b'], "Inválido: Sequência não permitida pelas regras."),
        (['b', 'b'], "Inválido: Não há regra para gerar dois 'b's consecutivos."),
        (['c', 'd'], "Inválido: Após 'c A', A não pode derivar em 'd' diretamente nesse contexto."),
        ([], "Inválido: Entrada vazia (gramática não gera a sentença vazia)."),
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