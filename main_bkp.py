from lexer import lexer
from parser_ import Parser
from semantic import semantic_check
from ir_generator import generate_ir
from optimizer import optimize
from executor import execute

def main():
    code = input("Digite a expressão matemática: ")
    print("\n=== Etapa 1: Análise Léxica ===")
    tokens = lexer(code)
    print(tokens)

    print("\n=== Etapa 2: Análise Sintática ===")
    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)

    print("\n=== Etapa 3: Análise Semântica ===")
    semantic_check(ast)
    print("Semântica válida")

    print("\n=== Etapa 4: Geração de Código Intermediário ===")
    ir, result = generate_ir(ast)
    for instr in ir:
        print(instr)

    print("\n=== Etapa 5: Otimização ===")
    optimized_ir = optimize(ir)
    for instr in optimized_ir:
        print(instr)

    print("\n=== Etapa 6: Execução ===")
    env = execute(optimized_ir)
    print(f"Resultado final: {env[result]}")

if __name__ == "__main__":
    main()
