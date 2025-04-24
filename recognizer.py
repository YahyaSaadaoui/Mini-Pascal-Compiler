# recognizer.py
"""
Low-level token recognisers – function‐based port of
lexicalAnalyser.Recognizer.java (no classes, no OO).

Each function analyses the current char (Global.carlu), consumes the
necessary characters via ``reader.lire_car()`` and returns the detected
LexicalUnit, while updating the shared Global fields just like the Java
code.

Usage pattern in lexer.py
-------------------------
    import recognizer as rec
    ...
    c = G.get_carlu()
    if c.isdigit():
        return rec.reco_int(reader)
    elif c.isalpha():
        return rec.reco_ident_or_reserve_word(reader)
    ...
"""

from global_state import Global as G
from constants import LexicalUnit as LU
from error import (
    raise_error,
    EXCEED_LENGTH_INT,
    EXCEED_LENGTH_STRING,
    EXCEED_LENGTH_IDENT,
)
from keywords import is_keyword
import symbol as sym  # symbol.py


# ─────────────────────────── integer literal ────────────────────────────────
def reco_int(reader):
    num_txt = []
    while G.get_carlu().isdigit():
        num_txt.append(G.get_carlu())
        reader.lire_car()

    value = int("".join(num_txt))
    if value > G.MAX_INT:
        raise_error(EXCEED_LENGTH_INT, "integer literal too large")

    G.set_nombre(value)
    return LU.ent


# ───────────────────────────── string literal ───────────────────────────────
def reco_string(reader):
    # we are positioned on the opening quote '
    reader.lire_car()  # skip it
    chars, prev = [], " "

    while not (G.get_carlu() == "'" and prev != "\\"):
        chars.append(G.get_carlu())
        prev = G.get_carlu()
        reader.lire_car()

    reader.lire_car()  # consume closing '
    string_val = "".join(chars)

    if len(string_val) > G.LONG_MAX_CHAINE:
        raise_error(EXCEED_LENGTH_STRING, "string literal too long")

    G.set_chaine(string_val)
    return LU.ch


# ───────────────────── identifier OR reserved keyword ───────────────────────
def reco_ident_or_reserve_word(reader):
    buf = []
    while (
        G.get_carlu().isalnum() or G.get_carlu() == "_"
    ):
        buf.append(G.get_carlu())
        reader.lire_car()

    word = "".join(buf)
    if len(word) > G.LONG_MAX_INDENT:
        raise_error(EXCEED_LENGTH_IDENT, "identifier too long")

    G.set_chaine(word.upper())
    return LU.motcle if is_keyword(word) else LU.ident


# ─────────────────────────────── symbols ────────────────────────────────────
def reco_symbol(reader):
    current = G.get_carlu()
    comp = current
    last_char_consumed = True

    if sym.is_part_of_compose_symbol(comp):
        reader.lire_car()
        nxt = G.get_carlu()
        if sym.is_symbol(nxt) and nxt in sym.get_compose_symbol_next_symbol()[comp]:
            comp += nxt
        else:
            last_char_consumed = False

    if last_char_consumed:
        reader.lire_car()

    lex_unit = sym.get_symbol_to_lexical_unit().get(comp)
    if lex_unit is None:
        raise RuntimeError(f"Le symbole '{comp}' n'est pas une unité lexicale")

    return lex_unit
