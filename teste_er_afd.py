from ExpresaoRegular import ExpressaoRegular

ER = ExpressaoRegular("a(b|a)*b")
A = ER.thompson()

afd = A.determinizar()
print(afd)

palavras = ["ab", "aab", "aaab", "b", "a", "abb", "baab"]
for palavra in palavras:
    if afd.aceita(palavra):
        print(f"A palavra '{palavra}' foi aceita.")
    else:
        print(f"A palavra '{palavra}' foi rejeitada.")