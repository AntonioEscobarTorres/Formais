# Analisador Léxico

Este projeto implementa um analisador léxico capaz de reconhecer tokens a partir de um conjunto de expressões regulares e uma lista de palavras de entrada. Ele constrói um Autômato Finito Não Determinístico (AFN) unificado, o converte para um Autômato Finito Determinístico (AFD) e utiliza este AFD para realizar a análise léxica das entradas fornecidas.

## Como Executar

Para executar o analisador léxico, você precisará ter o Python instalado. Navegue até o diretório raiz do projeto pelo terminal e execute o arquivo principal.

```bash
python main.py
```

## Entrada

As configurações de entrada para o analisador devem ser fornecidas através de arquivos de texto localizados na pasta Testes/ (relativa à raiz do projeto).

1. Expressões Regulares (Testes/expressoes.txt)

    Este arquivo deve conter as definições das expressões regulares (ERs) que o analisador utilizará para reconhecer os tokens. O nome do token e a expressão devem estar juntos e sem espaços entre si e no final. Cada linha deve seguir o formato:

    nome_do_token:expressao_regular

        nome_do_token: O nome do token que será associado à expressão regular (ex: id, num, palavra_reservada).

        expressao_regular: A expressão regular em si.

    Exemplo de Testes/expressoes.txt:

        id:[a-zA-Z_][a-zA-Z0-9_]*
        num_int:[1-9]([0-9])*|0

2. Palavras de Teste (Testes/testes.txt)

    Este arquivo deve conter a lista de palavras (lexemas) que você deseja que o analisador processe. Cada palavra deve estar em uma nova linha.

    Exemplo de Testes/testes.txt:

        if
        contador
        123
        else
        _variavel
        while_loop
        456abc

## Saída

Durante a execução, o analisador pode imprimir informações sobre o processo no console. Além disso, os seguintes arquivos serão gerados (ou sobrescritos) na raiz do projeto:

1. Arquivo do AFD (afd_salvo.txt)

    O Autômato Finito Determinístico (AFD) gerado pelo analisador a partir das expressões regulares fornecidas será salvo automaticamente neste arquivo. Ele conterá a representação textual do AFD.

2. Tabela de Símbolos (tabela_de_simbolos.txt)

    A tabela de símbolos, contendo os lexemas reconhecidos e seus respectivos tokens, será salva neste arquivo. Cada linha terá o formato <lexema,token>.

## Estrutura de Arquivos

```text
raiz_do_projeto/
├── main.py                     # Seu arquivo executável principal
├── src/                          # Pasta com os módulos do analisador
│   ├── AnalisadorLexico.py
│   ├── Automato.py
│   ├── Estado.py
│   ├── Transicao.py
│   ├── ExpressaoRegular.py
│   └── LeitorDeEr.py
│   └── testes_unitarios/         # Testes para as classes
│  
├── Testes/
│   ├── expressoes.txt            # Arquivo de entrada para as ERs
│   └── testes.txt                # Arquivo de entrada para as palavras a serem analisadas
├── afd_salvo.txt               # Arquivo de saída gerado com o AFD
└── tabela_de_simbolos.txt      # Arquivo de saída gerado com a tabela de símbolos
```