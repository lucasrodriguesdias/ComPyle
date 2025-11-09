import math

def execute(ir):
    env = {}
    for instr in ir:
        op = instr[0]
        if op == "LOAD_CONST":
            env[instr[2]] = instr[1]
        elif op == "LOAD_VAR":
            env[instr[2]] = getattr(math, instr[1])
        elif op == "BINOP":
            a, b = env[instr[2]], env[instr[3]]
            env[instr[4]] = eval(f"a {instr[1]} b")
        elif op == "CALL_FUNC":
            func = getattr(math, instr[1])
            args = [env[a] for a in instr[2]]
            env[instr[3]] = func(*args)
    return env
