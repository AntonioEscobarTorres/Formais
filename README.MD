# Compilador

    Este projeto implementa um analisador léxico e um analisador sintático, integrando ambos para permitir o processamento completo de código-fonte com base em uma gramática e expressões regulares fornecidas.

    O analisador léxico é capaz de reconhecer tokens a partir de um conjunto de expressões regulares e uma lista de palavras de entrada. Ele constrói um Autômato Finito Não Determinístico (AFN) unificado, converte-o em um Autômato Finito Determinístico (AFD) e utiliza este AFD para realizar a análise léxica das entradas fornecidas.

    O analisador sintático, por sua vez, utiliza a tabela SLR gerada a partir de uma Gramática Livre de Contexto (GLC) para validar a estrutura sintática da lista de tokens produzida pelo léxico. A integração entre os dois módulos permite que o sistema analise um programa desde a leitura do código-fonte até a validação sintática completa, armazenando os símbolos reconhecidos e reportando erros caso a entrada não esteja conforme a gramática definida.

## Como Executar

Para executar o analisador léxico, você precisará ter o Python instalado. Navegue até o diretório raiz do projeto pelo terminal e execute o arquivo principal.

```bash
python main.py
```

## Entrada

As configurações de entrada para o analisador devem ser fornecidas através de arquivos de texto localizados na pasta Testes/ (relativa à raiz do projeto).

1. Expressões Regulares (Testes/expressoes1.txt)

    Este arquivo deve conter as definições das expressões regulares (ERs) que o analisador utilizará para reconhecer os tokens. O nome do token e a expressão devem estar juntos e sem espaços entre si e no final. Cada linha deve seguir o formato:

    nome_do_token:expressao_regular

        nome_do_token: O nome do token que será associado à expressão regular (ex: id, num, palavra_reservada).

        expressao_regular: A expressão regular em si.

    Exemplo de Testes/expressoes.txt:

        id:[a-zA-Z_][a-zA-Z0-9_]*
        num_int:[1-9]([0-9])*|0

2. Palavras de Teste (Testes/palavras_reservadas.txt)

    Este arquivo deve conter a lista de palavras (lexemas) que você deseja que o analisador processe. Cada palavra deve estar em uma nova linha.

    Exemplo de Testes/palavras_reservadas.txt:

        if
        contador
        123
        else
        _variavel
        while_loop
        456abc

3. Gramatica de Teste (Testes/gramatica_completa.txt)

    Este arquivo contém uma gramática que simula o funcionamento de uma linguagem.

    Exemplo de Testes/gramatica_completa.txt:

        <programa> ::= <declaracoes> "." 

        <declaracoes> ::= <dcl_const> <dcl_var>

        <dcl_const> ::= const <tipo_pre_def> id "=" <constante> ";" <dcl_const>
        <dcl_const> ::= &

        <dcl_var> ::= var <lid> ":" <tipo> ";" <dcl_var> 
        <dcl_var> ::= &

4. Exemplo de Código Fonte (Testes/codigo_fonte.txt)

    Este arquivo e suas variações contem um exemplo de código que será aceito pela grámatica_completa, o código deve estar totalmente separado palavras juntas serão considerados erros sintáticos ( "var()" por exemplo, o correto seria "var ( )"), ele deve ser executado junto com o arquivo expressoes.txt e gramatica_completa.txt

    Exemplo de Testes/codigo_fonte.txt:
        var contador : inteiro ;
        var resultado : real ;

        inicio
            contador := 10 ;
            se contador > 0 entao
                resultado := contador * 2
        fim .

## Saída

Durante a execução, o analisador pode imprimir informações sobre o processo no console. Além disso, os seguintes arquivos serão gerados (ou sobrescritos) na pasta arquivos_gerados:

1. Arquivo do AFD (afd_salvo.txt)

    O Autômato Finito Determinístico (AFD) gerado pelo analisador a partir das expressões regulares fornecidas será salvo automaticamente neste arquivo. Ele conterá a representação textual do AFD.

2. Tabela de Símbolos (tabela_de_simbolos.txt)

    A tabela de símbolos, contendo os lexemas reconhecidos e seus respectivos tokens, será salva neste arquivo. Cada linha terá o formato <lexema,token>.

3. Tabela de Símbolos (tabela_de_simbolos_atualizada.txt)

    A tabela de símbolos, atualizada após passar pelo compilador. Cada linha terá o formato <lexema,token>.

4. Tabela SLR (tabela_slr.txt)

    A tabela SLR, contendo a tabela gerada na analise sintática, será salva neste arquivo. Cada linha terá o formato (0, 'xxx'): ('shift', 2), por exemplo.

## Estrutura de Arquivos

```text
FORMAIS/
│
├── arquivos_gerados/                    # Pasta reservada para saídas/relatórios
│   └── tabela_de_simbolos.txt 
├── src/
│   ├── Analisador_Lexico/              # Módulos do analisador léxico
│   │   ├── AnalisadorLexico.py
│   │   ├── Automato.py
│   │   ├── Estado.py
│   │   ├── ExpressaoRegular.py
│   │   ├── LeitorDeEr.py
│   │   └── Transicao.py
│   ├── Analisador_Sintatico/           # Módulos do analisador sintático
│   │   ├── AnalisadorSintatico.py
│   │   ├── Gramatica.py
│   │   ├── ItemLR0.py
│   │   ├── LeitorDeGramatica.py
│   │   ├── Producao.py
│   │   ├── SLR.py
│   │   ├── Simbolo.py
│   │   └── TipoSimbolo.py                 # Arquivo do compilador (integração entre sintático x léxico)
│   ├── testes_unitarios/               # Arquivos de teste
│   │   ├── teste_afd.py
│   │   ├── teste_analizador.py
│   │   ├── teste_analizador_sintatico.py
│   │   ├── teste_closure.py
│   │   ├── teste_closure2.py
│   │   ├── teste_colecao_canonica.py
│   │   ├── teste_det.py
│   │   ├── teste_enumiao.py
│   │   ├── teste_first.py
│   │   ├── teste_first2.py
│   │   ├── teste_follow.py
│   │   ├── teste_follow2.py
│   │   ├── teste_integracao_canonico_parser.py
│   │   └── teste_slr.py
│   └── compilador.py  
└── main.py    # Arquivo principal
```