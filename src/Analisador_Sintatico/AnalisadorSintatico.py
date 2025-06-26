import sys
import os
from pprint import pprint

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Analisador_Sintatico.Gramatica import Gramatica
from Analisador_Sintatico.LeitorDeGramatica import LeitorDeGramatica
from Analisador_Sintatico.SLR import SLRParser

class AnalisadorSintatico:

    def __init__(self, caminho_gramatica: str):
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
        
        colecao_canonica, _ = self.gramatica_obj.calcular_colecao_canonica()
        colecao_para_parser = [conj for _, conj in colecao_canonica]
        follow_para_parser = self.gramatica_obj.calcular_follow()

        
        self.parser_slr = SLRParser(self.gramatica_obj, colecao_para_parser, follow_para_parser)
        #self.gramatica_obj.imprimir_itens_canonicos()
        #self.parser_slr.imprimir_tabela()

    def analisar(self, lista_tokens: list[str]):
        if not self.parser_slr:
            print("❌ Erro: O parser SLR não foi inicializado.")
            return False
        print("")
        return self.parser_slr.parse(lista_tokens)

    def salvar_tabela_de_analise(self, nome_arquivo="./arquivos_gerados/tabela_slr.txt"):
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
        return self.palavras_reservadas
