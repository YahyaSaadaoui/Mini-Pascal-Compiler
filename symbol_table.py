# symbol_table.py
"""
Procedural translation of tableIdentifier.IdentifierTable + IdentifierEntry.

Everything lives at module level: a list that stores all identifier
records (dictionaries) and a companion list that keeps the indexes of
those records sorted alphabetically by the identifier's name.  Public
helper functions mimic the methods used by the Java compiler pipeline.
"""

from __future__ import annotations

from pprint import pprint
from typing import Any, Dict, List

from constants import IdentifierType

# ────────────────────────── module-level storage ─────────────────────────
_MAX_IDENTIFIERS: int = 100
_table: List[Dict[str, Any]] = []          # each entry is a dict
_sorted_indexes: List[int] = []            # positions of _table sorted by name


# ───────────────────────────── internals ─────────────────────────────────
def _make_entry(name: str, id_type: IdentifierType) -> Dict[str, Any]:
    """Return a brand-new identifier record with default fields."""
    return {
        "name": name,
        "type": id_type,
        # optional / later-filled fields ↓
        "value": None,
        "address": None,
        "var_type": None,
        "dimension": None,
        "passage_mode": None,
        "parameter_count": None,
        "return_type": None,
    }


def _insert_into_sorted_indexes(new_idx: int) -> None:
    """Keep `_sorted_indexes` alphabetically ordered by identifier name."""
    new_name = _table[new_idx]["name"]
    pos = 0
    while pos < len(_sorted_indexes) and _table[_sorted_indexes[pos]]["name"] < new_name:
        pos += 1
    _sorted_indexes.insert(pos, new_idx)


# ───────────────────────────── API functions ─────────────────────────────
def reset() -> None:
    """Clear the table — handy for unit tests."""
    _table.clear()
    _sorted_indexes.clear()


def size() -> int:
    return len(_table)


def search(name: str) -> int:
    """
    Binary search in the **sorted index list**.
    Returns the table index or -1 if absent.
    """
    left, right = 0, len(_sorted_indexes) - 1
    while left <= right:
        mid = (left + right) // 2
        mid_name = _table[_sorted_indexes[mid]]["name"]
        if mid_name == name:
            return _sorted_indexes[mid]
        if mid_name < name:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def insert(name: str, id_type: IdentifierType) -> int:
    """Add a new identifier; raise RuntimeError on overflow or duplicates."""
    if size() >= _MAX_IDENTIFIERS:
        raise RuntimeError("Table des identificateurs pleine")

    if search(name) != -1:
        raise RuntimeError(f"Identificateur déjà existant: {name}")

    entry = _make_entry(name, id_type)
    _table.append(entry)
    new_index = size() - 1
    _insert_into_sorted_indexes(new_index)
    return new_index


def get_entry(index: int) -> Dict[str, Any] | None:
    if 0 <= index < size():
        return _table[index]
    return None


def get_address_of(var_name: str) -> int:
    idx = search(var_name)
    entry = get_entry(idx)
    if entry is None or entry["address"] is None:
        raise RuntimeError(f"Adresse inconnue pour la variable {var_name}")
    return entry["address"]


def display_table() -> None:
    print("\nTable des Identificateurs:")
    print("-------------------------")
    for i, rec in enumerate(_table):
        print(f"Index {i}: {rec}")

    print("\nTable d'Index Triée:")
    print("------------------")
    for pos, idx in enumerate(_sorted_indexes):
        print(f"Position {pos}: Index {idx} ({_table[idx]['name']})")


# ─────────────────────────── convenience setters ─────────────────────────
# The compiler front-end can call these to mutate fields of an entry
# without importing the whole record structure.

def set_value(index: int, value: int) -> None:
    _table[index]["value"] = value


def set_address(index: int, address: int) -> None:
    _table[index]["address"] = address


def set_var_type(index: int, var_type: int) -> None:
    _table[index]["var_type"] = var_type


def set_dimension(index: int, dimension: int) -> None:
    _table[index]["dimension"] = dimension


def set_passage_mode(index: int, mode: str) -> None:
    _table[index]["passage_mode"] = mode


def set_parameter_count(index: int, count: int) -> None:
    _table[index]["parameter_count"] = count


def set_return_type(index: int, return_type: int) -> None:
    _table[index]["return_type"] = return_type
