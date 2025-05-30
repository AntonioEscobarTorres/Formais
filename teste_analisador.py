from AnalisadorLexico import AnalisadorLexico

expressoes = [
    ("NUM", "a*"),
    ("AB_TOKEN", "ab"),
    ("BnoINICIO", "b(a|b)*")
]


entrada = "aaaaaa ab b baaaaab aaa ab acd"


analisador = AnalisadorLexico()


print(30*"-")

analisador.print_tabela_de_simbolos()
