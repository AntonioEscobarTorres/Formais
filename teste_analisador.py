from AnalisadorLexico import AnalisadorLexico

expressoes = [
    ("NUM", "a*"),
    ("AB_TOKEN", "ab"),
    ("BnoINICIO", "b(a|b)*")
]



analisador = AnalisadorLexico(expressoes)

print(analisador.reconhecer_token("aaaaaa"))  # Deve retornar NUM
print(analisador.reconhecer_token("ab"))   # Deve retornar AB_TOKEN
print(analisador.reconhecer_token("b"))    # Deve retornar "Token não reconhecido"
print(analisador.reconhecer_token("baaaab"))    # Deve retornar BnoINICIO"