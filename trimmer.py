# trimmer.py
"""
Procedural equivalent of lexicalAnalyser.SeparatorTrimmer (Java).

It removes:
    • contiguous spaces / tabs
    • Pascal-style brace comments { … }  (nesting supported)

API
----
trim(reader)               # mutates global_state.carlu via reader.lire_car()
is_space(ch)               # predicate helpers
is_start_of_commentary(ch)
is_end_of_commentary(ch)
"""

from typing import List

from global_state import Global  # mirrors shared.Global.java


# ──────────────────────────── predicates ────────────────────────────────
def is_space(ch: str) -> bool:
    return ch in (" ", "\t")


def is_start_of_commentary(ch: str) -> bool:
    return ch == "{"


def is_end_of_commentary(ch: str) -> bool:
    return ch == "}"


# ────────────────────────── public interface ────────────────────────────
def trim(reader) -> None:
    """
    Skip over whitespace or brace-delimited comments in the input stream.

    Parameters
    ----------
    reader : SourceReader-like object
        Must expose a ``lire_car()`` method that advances one character and
        updates ``Global.carlu`` (just like the Java implementation).
    """
    if is_space(Global.carlu):
        _trim_space(reader)
    elif is_start_of_commentary(Global.carlu):
        _trim_commentary(reader)


# ───────────────────────────── helpers ──────────────────────────────────
def _trim_space(reader) -> None:
    while is_space(Global.carlu):
        reader.lire_car()


def _trim_commentary(reader) -> None:
    # support nested { … } comments
    stack: List[str] = ["{"]  # sentinel for the opening brace we are on
    reader.lire_car()         # consume the first '{'

    while stack:
        if is_start_of_commentary(Global.carlu):
            stack.append("{")
        elif is_end_of_commentary(Global.carlu):
            stack.pop()
        reader.lire_car()
