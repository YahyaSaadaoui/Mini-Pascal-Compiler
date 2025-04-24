# interpreter.py

from constants import OperationCode
from memory import create_memory_word

def interpret(virtual_memory):
    p_code = virtual_memory["p_code"]
    mem_var = virtual_memory["mem_var"]
    pilex = []
    head_pilex = -1
    index = 0

    while OperationCode.from_code(p_code[index]["value"]) != OperationCode.STOP:
        op = OperationCode.from_code(p_code[index]["value"])

        if op == OperationCode.ADDI:
            pilex[head_pilex - 1] += pilex[head_pilex]
            head_pilex -= 1
            index += 1

        elif op == OperationCode.SOUS:
            pilex[head_pilex - 1] -= pilex[head_pilex]
            head_pilex -= 1
            index += 1

        elif op == OperationCode.MULT:
            pilex[head_pilex - 1] *= pilex[head_pilex]
            head_pilex -= 1
            index += 1

        elif op == OperationCode.DIV:
            divisor = pilex[head_pilex]
            if divisor == 0:
                print(f"Runtime Error: Division by zero at index {index}")
                return
            pilex[head_pilex - 1] //= divisor
            head_pilex -= 1
            index += 1

        elif op == OperationCode.MOIN:
            pilex[head_pilex] = -pilex[head_pilex]
            index += 1

        elif op == OperationCode.AFFE:
            addr = pilex[head_pilex]
            val = pilex[head_pilex - 1]
            mem_var[addr] = create_memory_word(val)
            index += 1

        elif op == OperationCode.LIRE:
            addr = pilex[head_pilex]
            if 0 <= addr < len(mem_var):
                val = int(input("Input> "))
                mem_var[addr]["value"] = val
            else:
                print(f"Runtime Error: Invalid address {addr} for LIRE at index {index}")
                return
            head_pilex -= 1
            index += 1

        elif op == OperationCode.ECRL:
            print()
            index += 1

        elif op == OperationCode.ECRE:
            print(pilex[head_pilex], end='')
            head_pilex -= 1
            index += 1

        elif op == OperationCode.ECRC:
            index += 1
            while p_code[index]["value"] != OperationCode.FINC.value:
                if index >= len(p_code):
                    print(f"Runtime Error: ECRC string not terminated by FINC at index {index}")
                    return
                print(chr(p_code[index]["value"]), end='')
                index += 1
            index += 1

        elif op == OperationCode.EMPI:
            head_pilex += 1
            if index + 1 >= len(p_code):
                print(f"Runtime Error: Missing operand for EMPI at index {index}")
                return
            pilex.append(p_code[index + 1]["value"])
            index += 2

        elif op == OperationCode.CONT:
            addr = pilex[head_pilex]
            if 0 <= addr < len(mem_var):
                pilex[head_pilex] = mem_var[addr]["value"]
            else:
                print(f"Runtime Error: Invalid address {addr} for CONT at index {index}")
                return
            index += 1

        elif op == OperationCode.FINC:
            print(f"Runtime Error: Unexpected FINC outside ECRC at index {index}")
            return

        else:
            print(f"Warning: Unhandled OperationCode {op.name} at index {index}")
            index += 1
