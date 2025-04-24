# source_reader.py
"""
A minimal, non-OO replacement for lexicalAnalyser.SourceReader.java.

The module keeps a single open file handle and a cursor that walks
through it character-by-character.  It cooperates with `global_state`
(the old `shared.Global`) by updating the current character and the
line counter exactly like the original Java version.
"""

from pathlib import Path
from typing import TextIO

from global_state import Global as G
from error import raise_error, UNKNOWN_ERROR   # adapt the constant name if needed


# ────────────────────────── module-level state ───────────────────────────
_reader: TextIO | None = None        # the underlying buffered reader
_current_line: str | None = None     # text of the line presently being scanned
_line_index: int = 0                 # position *within* _current_line


# ───────────────────────────── helpers ───────────────────────────────────
def _init_reader() -> TextIO:
    try:
        return Path(G.get_source()).open(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"Impossible d'ouvrir {G.get_source()!r}: {exc}") from exc


def _set_next_line() -> None:
    """Advance to the next line of the file (or EOF)."""
    global _current_line
    _current_line = _reader.readline() if _reader else None
    # strip trailing newline so indices match Java version
    if _current_line and _current_line.endswith("\n"):
        _current_line = _current_line[:-1]


# ────────────────────────── public interface ─────────────────────────────
def init() -> None:
    """Open the source file whose path lives in `G.source`."""
    global _reader, _line_index
    _reader = _init_reader()
    _set_next_line()
    _line_index = 0


def close() -> None:
    if _reader:
        try:
            _reader.close()
        finally:
            # reset state so `init()` can be called again if needed
            globals()['_reader'] = None


def lire_car() -> None:
    """
    Read the next character from the source and store it in Global.carlu.

    This mirrors SourceReader.lireCar() in the original Java code.
    """
    global _line_index

    # when we reach the end of the current line, advance to the next
    if _current_line is not None and _line_index == len(_current_line):
        G.set_num_ligne(G.get_num_ligne() + 1)
        _line_index = 0
        _set_next_line()

    # EOF → signal the generic error used by the Java code (number 1)
    if _current_line is None:
        # mimic the debug print the Java version made just before erroring
        print(f"{G.get_chaine()} {G.get_carlu()}")
        raise_error(UNKNOWN_ERROR, "")        # change constant if your `error.py` differs
        return

    # store current character in global state and move the cursor forward
    G.set_carlu(_current_line[_line_index])
    _line_index += 1


# initialise automatically so that other modules can immediately call
