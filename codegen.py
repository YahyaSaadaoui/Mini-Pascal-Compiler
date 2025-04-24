from constants import *
import global_state as g
from memory import new_memory_word, get_virtual_memory

co = 0


def get_co():
    return co


def set_co(val):
    global co
    co = val


def add_line(code, vm=None):
    if vm is None:
        vm = get_virtual_memory()
    vm["p_code"].append(new_memory_word(code))
    set_co(get_co() + 1)


def add_line_word(word, vm=None):
    if vm is None:
        vm = get_virtual_memory()
    vm["p_code"].append(word)
    set_co(get_co() + 1)


def get_line(index, vm=None):
    if vm is None:
        vm = get_virtual_memory()
    return vm["p_code"][index]


def handle_identifier_table(table, vm=None):
    if vm is None:
        vm = get_virtual_memory()
    i = 0
    while table.get_entry(i) is not None:
        if table.get_entry(i).get_type() == "VARIABLE":
            vm["mem_var"].append(new_memory_word(0))
        i += 1


def write_code_file(file_name, vm=None):
    if vm is None:
        vm = get_virtual_memory()
    from pathlib import Path
    content = []
    content.append(f"{len(vm['mem_var'])} {len(vm['p_code'])}")
    index = 0
    while get_line(index, vm).get_value() != STOP:
        op = OperationCode.from_code(get_line(index, vm).get_value())
        line = [op.name]
        if op == EMPI:
            index += 1
            line.append(str(get_line(index, vm).get_value()))
        elif op == ECRC:
            index += 1
            chars = []
            while get_line(index, vm).get_value() != FINC:
                chars.append(chr(get_line(index, vm).get_value()))
                index += 1
            line.append(f"'{''.join(chars)}'")
            line.append(OperationCode.from_code(get_line(index, vm).get_value()).name)
        content.append(" ".join(line))
        index += 1
    content.append(OperationCode.from_code(get_line(index, vm).get_value()).name)
    Path(file_name).write_text("\n".join(content), encoding="utf-8")
    print(f"Successfully wrote to file: {Path(file_name).absolute()}")


def gen_code_affectation(vm, table, var_name):
    add_line(EMPI, vm)
    add_line(table.get_address_of(var_name), vm)
    add_line(AFFE, vm)


def gen_code_read(vm, table, var_name):
    add_line(EMPI, vm)
    add_line(table.get_address_of(var_name), vm)
    add_line(LIRE, vm)


def gen_code_write(vm):
    add_line(ECRL, vm)


def gen_code_print_string(vm):
    add_line(ECRC, vm)
    for ch in g.get_chaine():
        add_line(ord(ch), vm)
    add_line(FINC, vm)


def gen_code_print_expr(vm):
    add_line(ECRE, vm)


def gen_code_expr(vm):
    if vm["pilop"]:
        add_line(vm["pilop"].pop().get_value(), vm)


def gen_code_binop(vm):
    if g.get_unilex() == PLUS:
        vm["pilop"].append(new_memory_word(ADDI))
    elif g.get_unilex() == MOINS:
        vm["pilop"].append(new_memory_word(SOUS))
    elif g.get_unilex() == MULT:
        vm["pilop"].append(new_memory_word(MULTI))
    elif g.get_unilex() == DIVI:
        vm["pilop"].append(new_memory_word(DIV))


def gen_code_term_int(vm):
    add_line(EMPI, vm)
    add_line(g.get_nombre(), vm)


def gen_code_term_ident(vm, table):
    add_line(EMPI, vm)
    if table.is_constant(g.get_chaine()):
        add_line(table.get_constant_value(g.get_chaine()), vm)
    else:
        add_line(table.get_address_of(g.get_chaine()), vm)
        add_line(CONT, vm)


def gen_code_term_minus(vm):
    add_line(MOIN, vm)
