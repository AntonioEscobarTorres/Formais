import re
from .Producao import Producao
from .Simbolo import Simbolo
from .TipoSimbolo import TipoSimbolo

class LeitorDeGramatica:
    @staticmethod
    def ler_arquivo(caminho_arquivo: str):
        producoes_obj = []
        todos_nao_terminais = set()
        todos_terminais = set()
        simbolo_inicial = None

        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                # Ignora linhas vazias, comentários ou linhas sem o separador
                if not linha or linha.startswith('#') or '::=' not in linha:
                    continue
                
                cabeca_bruta, corpo_str = [p.strip() for p in linha.split('::=', 1)]

                # Normaliza a cabeça da produção: <exemplo> -> EXEMPLO
                if cabeca_bruta.startswith('<') and cabeca_bruta.endswith('>'):
                    cabeca = cabeca_bruta[1:-1].upper().replace('-', '_')
                else:
                    cabeca = cabeca_bruta

                todos_nao_terminais.add(cabeca)
                if simbolo_inicial is None:
                    simbolo_inicial = cabeca

                # Divide os corpos alternativos (separados por '|')
                corpos_alternativos = [c.strip() for c in corpo_str.split('|')]

                for corpo in corpos_alternativos:
                    simbolos_do_corpo = []
                    nomes_simbolos = corpo.split()
                    
                    # Trata a produção vazia (epsilon)
                    if not nomes_simbolos or (len(nomes_simbolos) == 1 and nomes_simbolos[0] == '&'):
                        # Assumindo que seu TipoSimbolo tem um valor para 'epsilon'
                        simbolos_do_corpo.append(Simbolo('&', TipoSimbolo.epsilon))
                        producoes_obj.append(Producao(cabeca, simbolos_do_corpo))
                        continue

                    for nome_simbolo_bruto in nomes_simbolos:
                        # Normaliza os símbolos do corpo da produção
                        if nome_simbolo_bruto.startswith('<') and nome_simbolo_bruto.endswith('>'):
                            tipo = TipoSimbolo.naoTerminal
                            # Converte <exemplo-nome> para EXEMPLO_NOME
                            nome_simbolo = nome_simbolo_bruto[1:-1].upper().replace('-', '_')
                            todos_nao_terminais.add(nome_simbolo)
                        else:
                            tipo = TipoSimbolo.terminal
                            # Verifica se o terminal está entre aspas
                            if (nome_simbolo_bruto.startswith('"') and nome_simbolo_bruto.endswith('"')) or \
                               (nome_simbolo_bruto.startswith("'") and nome_simbolo_bruto.endswith("'")):
                                # Extrai o conteúdo de dentro das aspas
                                nome_simbolo = nome_simbolo_bruto[1:-1]
                            else:
                                # Mantém o símbolo como está (ex: id, const)
                                nome_simbolo = nome_simbolo_bruto
                            
                            todos_terminais.add(nome_simbolo)
                        
                        simbolos_do_corpo.append(Simbolo(nome_simbolo, tipo))
                    
                    producoes_obj.append(Producao(cabeca, simbolos_do_corpo))
        
        # Identifica palavras reservadas (terminais alfanuméricos)
        palavras_reservadas = {t for t in todos_terminais if re.match(r'^[a-zA-Z_]\w*$', t)}

        return simbolo_inicial, todos_nao_terminais, todos_terminais, producoes_obj, palavras_reservadas
