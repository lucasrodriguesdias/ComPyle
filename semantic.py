import math

def semantic_check(node):
    if node[0] == 'num':
        return

    elif node[0] == 'var':
        if not hasattr(math, node[1]):
            raise NameError(f"Variável não reconhecida: {node[1]}")

    elif node[0] == 'func':
        func_name = node[1]
        if not hasattr(math, func_name):
            raise NameError(f"Função não reconhecida: {func_name}")
        for arg in node[2]:
            semantic_check(arg)

    elif node[0] == 'binop':
        semantic_check(node[2])
        semantic_check(node[3])
