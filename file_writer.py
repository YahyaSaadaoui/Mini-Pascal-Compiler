# file_writer.py

from constants import OperationCode
from pathlib import Path

def write_code_file(filename, virtual_memory):
    p_code = virtual_memory["p_code"]
    mem_var = virtual_memory["mem_var"]
    content = []

    # Write memory and code size
    content.append(f"{len(mem_var)} {len(p_code)}")

    index = 0
    while index < len(p_code) and p_code[index]["value"] != OperationCode.STOP.value:
        code_val = p_code[index]["value"]
        op = OperationCode.from_code(code_val)
        line = op.name

        if op == OperationCode.EMPI:
            index += 1
            line += f" {p_code[index]['value']}"

        elif op == OperationCode.ECRC:
            index += 1
            chars = []
            while p_code[index]["value"] != OperationCode.FINC.value:
                chars.append(chr(p_code[index]["value"]))
                index += 1
            line += f" '{''.join(chars)}' {OperationCode.FINC.name}"

        content.append(line)
        index += 1

    if index < len(p_code):
        content.append(OperationCode.from_code(p_code[index]["value"]).name)

    try:
        Path(filename).write_text("\n".join(content), encoding="utf-8")
        print(f"Successfully wrote to file: {Path(filename).absolute()}")
    except Exception as e:
        print(f"Error writing to file: {e}")
