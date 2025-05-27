from Automato import Automato
from Estado import Estado
from Transicao import Transicao

class ExpressaoRegular:
    def __init__(self, expressao: str):
        self.expressao = expressao

    def thompson(self):
        # Adiciona concatenação explícita (.)
        def add_concat_explicit(regex):
            resultado = ""
            for i in range(len(regex)):
                c1 = regex[i]
                resultado += c1
                if i + 1 < len(regex):
                    c2 = regex[i + 1]
                    if (c1.isalnum() or c1 == ')' or c1 == '*' or c1 == '?') and (c2.isalnum() or c2 == '('):
                        resultado += '.'
            return resultado

        # Converte para notação pós-fixa (shunting yard)
        def to_postfix(regex):
            precedencia = {'*': 3, '?': 3, '.': 2, '|': 1}
            output = []
            stack = []
            for c in regex:
                if c.isalnum():
                    output.append(c)
                elif c == '(':
                    stack.append(c)
                elif c == ')':
                    while stack and stack[-1] != '(':
                        output.append(stack.pop())
                    stack.pop()
                else:
                    while stack and stack[-1] != '(' and precedencia.get(stack[-1], 0) >= precedencia.get(c, 0):
                        output.append(stack.pop())
                    stack.append(c)
            while stack:
                output.append(stack.pop())
            return ''.join(output)

        # Funções de construção de AFN para cada operador
        def simbolo_afn(simbolo):
            s0 = Estado("q0")
            s1 = Estado("q1")
            trans = {Transicao(s0, simbolo, s1)}
            return Automato(2, s0, {s1}, trans, {simbolo})

        def uniao_afn(a1, a2):
            s0 = Estado("qU0")
            s1 = Estado("qU1")
            trans = set()
            trans.add(Transicao(s0, '&', a1.get_inicial()))
            trans.add(Transicao(s0, '&', a2.get_inicial()))
            for t in a1.get_transicoes():
                trans.add(t)
            for t in a2.get_transicoes():
                trans.add(t)
            for f in a1.get_finais():
                trans.add(Transicao(f, '&', s1))
            for f in a2.get_finais():
                trans.add(Transicao(f, '&', s1))
            estados = {s0, s1} | a1.get_estados() | a2.get_estados()
            alfabeto = a1.get_alfabeto() | a2.get_alfabeto()
            return Automato(len(estados), s0, {s1}, trans, alfabeto)

        def concat_afn(a1, a2):
            trans = set()
            for t in a1.get_transicoes():
                trans.add(t)
            for t in a2.get_transicoes():
                trans.add(t)
            for f in a1.get_finais():
                trans.add(Transicao(f, '&', a2.get_inicial()))
            estados = a1.get_estados() | a2.get_estados()
            alfabeto = a1.get_alfabeto() | a2.get_alfabeto()
            return Automato(len(estados), a1.get_inicial(), a2.get_finais(), trans, alfabeto)

        def estrela_afn(a):
            s0 = Estado("qE0")
            s1 = Estado("qE1")
            trans = set()
            trans.add(Transicao(s0, '&', a.get_inicial()))
            trans.add(Transicao(s0, '&', s1))
            for t in a.get_transicoes():
                trans.add(t)
            for f in a.get_finais():
                trans.add(Transicao(f, '&', a.get_inicial()))
                trans.add(Transicao(f, '&', s1))
            estados = {s0, s1} | a.get_estados()
            alfabeto = a.get_alfabeto()
            return Automato(len(estados), s0, {s1}, trans, alfabeto)

        def opcional_afn(a):
            s0 = Estado("qO0")
            s1 = Estado("qO1")
            trans = set()
            trans.add(Transicao(s0, '&', a.get_inicial()))
            trans.add(Transicao(s0, '&', s1))
            for t in a.get_transicoes():
                trans.add(t)
            for f in a.get_finais():
                trans.add(Transicao(f, '&', s1))
            estados = {s0, s1} | a.get_estados()
            alfabeto = a.get_alfabeto()
            return Automato(len(estados), s0, {s1}, trans, alfabeto)

        # Algoritmo principal
        regex = add_concat_explicit(self.expressao)
        postfix = to_postfix(regex)
        stack = []

        for c in postfix:
            if c.isalnum():
                stack.append(simbolo_afn(c))
            elif c == '*':
                a = stack.pop()
                stack.append(estrela_afn(a))
            elif c == '?':
                a = stack.pop()
                stack.append(opcional_afn(a))
            elif c == '.':
                a2 = stack.pop()
                a1 = stack.pop()
                stack.append(concat_afn(a1, a2))
            elif c == '|':
                a2 = stack.pop()
                a1 = stack.pop()
                stack.append(uniao_afn(a1, a2))
            else:
                raise ValueError(f"Símbolo inválido na regex: {c}")

        if len(stack) != 1:
            raise ValueError("Expressão regular mal formada.")

        return stack[0]
