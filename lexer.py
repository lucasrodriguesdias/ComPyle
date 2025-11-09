import re

TOKEN_SPECIFICATION = [
    ("NUMBER",   r"\d+(\.\d*)?"),
    ("NAME",     r"[A-Za-z_]\w*"),
    ("OP",       r"[+\-*/(),]"),
    ("SKIP",     r"[ \t]+"),
    ("MISMATCH", r"."),
]

def lexer(code):
    tokens = []
    regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPECIFICATION)
    for match in re.finditer(regex, code):
        kind = match.lastgroup
        value = match.group()
        if kind == "NUMBER":
            # Detecta se é inteiro ou float
            value = int(value) if '.' not in value else float(value)
        elif kind == "SKIP":
            continue
        elif kind == "MISMATCH":
            raise SyntaxError(f"Caractere inválido: {value}")
        tokens.append((kind, value))
    return tokens
