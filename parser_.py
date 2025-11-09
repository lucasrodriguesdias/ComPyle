class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def eat(self, kind=None):
        token = self.peek()
        if kind and token[0] != kind and token[1] != kind:
            raise SyntaxError(f"Esperado {kind}, encontrado {token}")
        self.pos += 1
        return token

    def parse(self):
        return self.expr()

    def expr(self):
        node = self.term()
        while self.peek()[1] in ('+', '-'):
            op = self.eat('OP')[1]
            right = self.term()
            node = ('binop', op, node, right)
        return node

    def term(self):
        node = self.factor()
        while self.peek()[1] in ('*', '/'):
            op = self.eat('OP')[1]
            right = self.factor()
            node = ('binop', op, node, right)
        return node

    def factor(self):
        tok_type, tok_val = self.peek()
        if tok_type == 'NUMBER':
            self.eat('NUMBER')
            return ('num', tok_val)

        elif tok_val == '(':
            self.eat('(')
            node = self.expr()
            self.eat(')')
            return node

        elif tok_type == 'NAME':
            name = self.eat('NAME')[1]
            if self.peek()[1] == '(':
                self.eat('(')
                args = [self.expr()]
                while self.peek()[1] == ',':
                    self.eat(',')
                    args.append(self.expr())
                self.eat(')')
                return ('func', name, args)
            return ('var', name)

        else:
            raise SyntaxError(f"Token inesperado: {tok_val}")
