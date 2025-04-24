virtual_memory = {
    "p_code": [{"value": 11}, {"value": 2}, {"value": 5}],  # etc.
    "mem_var": [{"value": 0}, {"value": 0}]  # MemoryWord-like dicts
}
# memory.py
"""
Pure-function replacement for Java's codeGenerator.VirtualMemory + MemoryWord.

A MemoryWord is just an int.  A "virtual memory" block is a plain dict
containing four lists:
    • mem_var  – data segment for variables
    • p_code   – list of instruction / operand words
    • pilex    – evaluation stack used by the interpreter
    • pilop    – operator stack used while parsing expressions
"""

MAX_SIZE_MEM = 10_000   # kept for parity with the Java constant


# ───────────────────────────── MemoryWord helper ────────────────────────────
def word(value: int) -> int:
    """Factory for a memory word (really just returns the int)."""
    return int(value)


# ──────────────────────────── VirtualMemory helper ──────────────────────────
def new_vm() -> dict:
    """
    Return a fresh virtual-memory dict.

    Keys ≈ Java fields:
        'mem_var' → list[int]   # variables area
        'p_code'  → list[int]   # generated P-code area
        'pilex'   → list[int]   # expression stack
        'pilop'   → list[int]   # operator stack
    """
    return {
        'mem_var': [],
        'p_code':  [],
        'pilex':   [],
        'pilop':   [],
    }


# ───────────────────────────── Convenience accessors ────────────────────────
def mem_var(vm): return vm['mem_var']
def p_code(vm):  return vm['p_code']
def pilex(vm):   return vm['pilex']
def pilop(vm):   return vm['pilop']


# ───────────────────────────── Mutator utilities ────────────────────────────
def add_mem_var(vm, initial: int = 0) -> None:
    """Allocate a new variable cell initialised to *initial*."""
    mem_var(vm).append(word(initial))


def push_p_code(vm, value: int) -> None:
    """Append an opcode or operand to the P-code list."""
    p_code(vm).append(word(value))


def p_code_at(vm, idx: int) -> int:
    """Return the instruction/operand stored at *idx* (no bounds checking)."""
    return p_code(vm)[idx]
