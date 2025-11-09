def generate_ir(node, temp_counter=[0]):
    if node[0] == 'num':
        t = f"t{temp_counter[0]}"
        temp_counter[0] += 1
        return [("LOAD_CONST", node[1], t)], t

    elif node[0] == 'var':
        t = f"t{temp_counter[0]}"
        temp_counter[0] += 1
        return [("LOAD_VAR", node[1], t)], t

    elif node[0] == 'func':
        code = []
        arg_temps = []
        for arg in node[2]:
            c, t = generate_ir(arg, temp_counter)
            code += c
            arg_temps.append(t)
        t = f"t{temp_counter[0]}"
        temp_counter[0] += 1
        code.append(("CALL_FUNC", node[1], arg_temps, t))
        return code, t

    elif node[0] == 'binop':
        left_code, left_t = generate_ir(node[2], temp_counter)
        right_code, right_t = generate_ir(node[3], temp_counter)
        t = f"t{temp_counter[0]}"
        temp_counter[0] += 1
        code = left_code + right_code + [("BINOP", node[1], left_t, right_t, t)]
        return code, t
