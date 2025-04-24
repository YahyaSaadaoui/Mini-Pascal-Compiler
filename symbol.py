# symbol.py
"""
Procedural utilities mirroring lexicalAnalyser.Symbol (Java).

The module exposes:
    - simple_symbols()                   → list[str]
    - compose_symbols()                  → list[str]
    - compose_symbol_next_symbol()       → dict[str, list[str]]
    - symbol_to_lexical_unit()           → dict[str, LexicalUnit]
    - is_part_of_compose_symbol(sym)     → bool
    - is_symbol(char)                    → bool
"""

from __future__ import annotations

from typing import Dict, List

from constants import LexicalUnit

# ────────────────────────── cached containers ────────────────────────────
_simple_symbols: List[str] | None = None
_compose_symbols: List[str] | None = None
_symbol_to_lexical_unit: Dict[str, LexicalUnit] | None = None
_compose_next: Dict[str, List[str]] | None = None


# ───────────────────────────── helpers ───────────────────────────────────
def _init_simple() -> List[str]:
    return [
        ",", ";", ".", ":", "(", ")", "<", ">", "=", "+", "-", "_", "*", "/"
    ]


def _init_compose() -> List[str]:
    return [">=", "<=", "<>", ":="]


def _init_compose_next() -> Dict[str, List[str]]:
    # first-character → list of legal seconds
    return {
        ">": ["="],
        "<": ["=", ">"],
        ":": ["="],
    }


def _init_symbol_to_lexical() -> Dict[str, LexicalUnit]:
    return {
        ",":  LexicalUnit.virg,
        ";":  LexicalUnit.ptvirg,
        ".":  LexicalUnit.point,
        ":":  LexicalUnit.deuxpts,
        "(":  LexicalUnit.parouv,
        ")":  LexicalUnit.parfer,
        "<":  LexicalUnit.inf,
        ">":  LexicalUnit.sup,
        "=":  LexicalUnit.eg,
        "+":  LexicalUnit.plus,
        "-":  LexicalUnit.moins,
        "*":  LexicalUnit.mult,
        "/":  LexicalUnit.divi,
        ">=": LexicalUnit.supe,
        "<=": LexicalUnit.infe,
        "<>": LexicalUnit.diff,
        ":=": LexicalUnit.aff,
    }


# ───────────────────────── public accessors ──────────────────────────────
def simple_symbols() -> List[str]:
    global _simple_symbols
    if _simple_symbols is None:
        _simple_symbols = _init_simple()
    return _simple_symbols


def compose_symbols() -> List[str]:
    global _compose_symbols
    if _compose_symbols is None:
        _compose_symbols = _init_compose()
    return _compose_symbols


def compose_symbol_next_symbol() -> Dict[str, List[str]]:
    global _compose_next
    if _compose_next is None:
        _compose_next = _init_compose_next()
    return _compose_next


def symbol_to_lexical_unit() -> Dict[str, LexicalUnit]:
    global _symbol_to_lexical_unit
    if _symbol_to_lexical_unit is None:
        _symbol_to_lexical_unit = _init_symbol_to_lexical()
    return _symbol_to_lexical_unit


# ─────────────────────────── convenience checks ──────────────────────────
def is_part_of_compose_symbol(symbol: str) -> bool:
    """
    Returns True if *symbol* (usually a single character like '<' or ':')
    could be the first part of a composed symbol.
    """
    return any(symbol in comp for comp in compose_symbols())


def is_symbol(char: str) -> bool:
    """True if *char* is one of the simple single-character symbols."""
    return char in simple_symbols()
