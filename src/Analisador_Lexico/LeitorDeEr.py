import re

class LeitorDeEr:
    @staticmethod
    def _traduzir_shorthands_para_er_valida(expressao_raw):
        # Define as expansões para as classes de caracteres
        lower_alpha_chars = [chr(ord('a') + i) for i in range(26)]
        upper_alpha_chars = [chr(ord('A') + i) for i in range(26)]
        digit_chars = [str(i) for i in range(10)]
        digits_1_9_chars = [str(i) for i in range(1, 10)]

        replacements = {
            r'\[a-z\]': '(' + '|'.join(lower_alpha_chars) + ')',
            r'\[A-Z\]': '(' + '|'.join(upper_alpha_chars) + ')',
            r'\[a-zA-Z\]': '(' + '|'.join(lower_alpha_chars + upper_alpha_chars) + ')',
            r'\[A-Za-z\]': '(' + '|'.join(upper_alpha_chars + lower_alpha_chars) + ')',
            r'\[0-9\]': '(' + '|'.join(digit_chars) + ')',
            r'\[1-9\]': '(' + '|'.join(digits_1_9_chars) + ')',
        }

        expressao_traduzida = expressao_raw
        for pattern, replacement in replacements.items():
            expressao_traduzida = re.sub(pattern, replacement, expressao_traduzida)

        return expressao_traduzida
    
    @staticmethod
    def ler_arquivo_er(caminho_arquivo):
        expressoes = []
        prioridade_atual = 0

        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()

        definicoes = conteudo.strip().split()

        for definicao in definicoes:
            if not definicao.strip():
                continue
                
            if ':' not in definicao:
                raise ValueError(f"Definição malformada (esperado 'nome:expressao'): {definicao}")

            nome, expressao_raw = definicao.split(":", 1)
            nome = nome.strip()
            expressao_raw = expressao_raw.strip()

            if not nome:
                raise ValueError(f"Nome do token vazio na definição: {definicao}")
            if not expressao_raw:
                raise ValueError(f"Expressão regular vazia para o token '{nome}': {definicao}")

            # Traduz a expressão lida
            expressao_traduzida = LeitorDeEr._traduzir_shorthands_para_er_valida(expressao_raw)
            
            # Adiciona à lista no formato (prioridade, nome_token, expressao_traduzida)
            expressoes.append((prioridade_atual, nome, expressao_traduzida))
            prioridade_atual += 1

        return expressoes

    @staticmethod
    def ler_arquivo_entrada(nome_arquivo):
        lexemas = []
        with open(nome_arquivo, "r") as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    # Divide a linha em lexemas separados por espaços
                    lexemas.extend(linha.split())
        return lexemas

