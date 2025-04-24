# lexer.py
#
# Functional re-write of Java's LexicalAnalyser.
# Relies on:  global_state, constants.LexicalUnit, source_reader, recognizer,
#             trimmer, symbol.
# No classes – just module-level state and functions.

from constants import LexicalUnit
import global_state as G
import source_reader
import recognizer
import trimmer
import symbol

# ---------------------------------------------------------------------------
# module-level reader handle (acts like the Java field `reader`)
_reader = None
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# public helpers
# ---------------------------------------------------------------------------
def init_lexer(src_path: str = "src/mini-pascal.txt") -> None:
    """
    Initialise global state and prime the first character.
    Must be called once before `analex()`.
    """
    global _reader
    G.set_num_line(0)
    G.set_source(src_path)

    _reader = source_reader.SourceReader()   # file opened inside
    _reader.read_char()                      # prime first char → G.set_carlu()


def close_lexer() -> None:
    """Close the underlying SourceReader (if any)."""
    if _reader is not None:
        _reader.close()
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# core scanner
# ---------------------------------------------------------------------------
def analex():
    """
    Scan the next token and return its LexicalUnit.
    Side-effects: updates many fields in `global_state`.
    Returns None when the sentinel `FIN.` is encountered (same as Java version).
    """
    if _reader is None:
        raise RuntimeError("Lexer not initialised – call init_lexer() first.")

    rec = recognizer                       # shorthand
    c = G.get_carlu()

    # EOF sentinel: the Java code stops on "FIN."
    if c == '.' and G.get_chain() == "FIN":
        G.running = False
        return None

    # → whitespace / comment
    if trimmer.is_space(c) or c == '{':
        trimmer.trim(_reader)
        return analex()                    # tail-recurse after trimming

    # → integer literal
    if c.isdigit():
        return rec.reco_int(_reader)

    # → identifier / reserved word
    if c.isalpha():
        return rec.reco_ident_or_reserve_word(_reader)

    # → string literal
    if c == "'":
        return rec.reco_string(_reader)

    # → symbol
    if c in symbol.get_simple_symbol():
        return rec.reco_symbol(_reader)

    # anything else is a lexical error
    raise RuntimeError(f"Unexpected character {c!r} at line {G.get_num_line()}")
# ---------------------------------------------------------------------------

