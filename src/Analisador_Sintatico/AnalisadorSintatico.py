import sys
import os
from pprint import pprint

# Adiciona o diretório pai ao path para permitir os imports
# (Assumindo que a estrutura é src/Analisador_Sintatico/ e este script está em src/testes/)
# Ajuste conforme a sua estrutura de execução.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Analisador_Sintatico.Gramatica import Gramatica
from Analisador_Sintatico.LeitorDeGramatica import LeitorDeGramatica
from Analisador_Sintatico.SLR import SLRParser

class AnalisadorSintatico:

    def __init__(self, caminho_gramatica: str):
        """
        Inicializa o analisador sintático a partir de um ficheiro de gramática.
        """
        self.caminho_gramatica = caminho_gramatica
        self.gramatica_obj = None
        self.palavras_reservadas = set()
        
        self.parser_slr = None

        self._processar()
        print("Analisador Sintático pronto.")

    def _processar(self):

        simbolo_inicial, nao_terminais, terminais, producoes, reservadas = \
            LeitorDeGramatica.ler_arquivo(self.caminho_gramatica)
        
        self.palavras_reservadas = reservadas
        
        self.gramatica_obj = Gramatica(simbolo_inicial, nao_terminais, terminais, producoes)
        
        producoes_para_parser = self.gramatica_obj.obter_producoes_formato_parser()
        colecao_para_parser = self.gramatica_obj.obter_colecao_formato_parser()
        follow_para_parser = self.gramatica_obj.calcular_follow()

        gramatica_mock = type('G', (), {'producoes': producoes_para_parser})()
        
        self.parser_slr = SLRParser(gramatica_mock, colecao_para_parser, follow_para_parser)

    def analisar(self, lista_tokens: list[str]):

        print(f"\nAnalisando entrada: {lista_tokens}")
        if not self.parser_slr:
            print("❌ Erro: O parser SLR não foi inicializado.")
            return False
            
        try:
            return self.parser_slr.parse(lista_tokens)
        except Exception as e:
            print(f"❌ Erro durante a análise sintática: {e}")
            return False

    def salvar_tabela_de_analise(self, nome_arquivo="tabela_slr.txt"):
        if not self.parser_slr or not hasattr(self.parser_slr, 'action'):
            print("Erro: Tabela de análise não foi gerada ou é inacessível.")
            return

        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                f.write("Tabela de Análise SLR Gerada\n")
                f.write("="*50 + "\n")
                f.write("\n--- Tabela ACTION ---\n")
                pprint(self.parser_slr.action, stream=f, width=120)
                f.write("\n--- Tabela GOTO ---\n")
                pprint(self.parser_slr.goto, stream=f, width=120)
            print(f"Tabela de análise salva com sucesso em '{nome_arquivo}'")
        except Exception as e:
            print(f"Erro ao salvar a tabela de análise: {e}")

    def get_palavras_reservadas(self) -> set:
        """Retorna o conjunto de palavras reservadas identificadas na gramática."""
        return self.palavras_reservadas
