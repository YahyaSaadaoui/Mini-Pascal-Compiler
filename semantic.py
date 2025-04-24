# semantic.py
"""
Semantic-level helpers that operate on the identifier table.

This is a direct, non-OO translation of
semanticAnalyzer.TableSemanticAnalyzer.java: every public Java method
is now a plain function that receives the active IdentifierTable
instance as its first argument.
"""

from constants import LexicalUnit, IdentifierType
from global_state import Global as G
from error import (
    raise_error,
    UNDECLARE_VARIABLE,
    SEMANTIC_ERROR,
    TYPE_ERROR,
)
# the IdentifierTable implementation created in symbol_table.py
import symbol_table as st


# ───────────────────────────── declarations ──────────────────────────────
def define_constant(table: st.IdentifierTable,
                    name: str,
                    ul: LexicalUnit,
                    value: int | None) -> bool:
    """Insert a new constant into *table*."""
    if table.search(name) != -1:
        print(f"Erreur: identificateur déjà déclaré: {name}")
        return False

    idx = table.insert(name, IdentifierType.CONSTANT)
    entry = table.get_entry(idx)

    if ul == LexicalUnit.ent:        # integer constant
        entry.var_type = 0
        entry.value = value
    else:                            # string constant
        entry.var_type = 1
        G.set_nb_const_chaine(G.get_nb_const_chaine() + 1)
        G.get_val_de_const_chaine().append(G.get_chaine())
        entry.value = G.get_nb_const_chaine()

    return True


def define_variable(table: st.IdentifierTable, name: str) -> bool:
    """Insert a new integer variable into *table*."""
    if table.search(name) != -1:
        print(f"Erreur: identificateur déjà déclaré: {name}")
        return False

    idx = table.insert(name, IdentifierType.VARIABLE)
    entry = table.get_entry(idx)

    G.increment_derniere_adresse_var_glob()
    entry.address = G.get_derniere_adresse_var_glob()
    entry.var_type = 0        # integer

    return True


# ───────────────────────────── inquiries ─────────────────────────────────
def is_declared(table: st.IdentifierTable, name: str) -> bool:
    """True iff *name* exists – otherwise raises UNDECLARE_VARIABLE."""
    if table.search(name) == -1:
        raise_error(UNDECLARE_VARIABLE, name)
        return False
    return True


def is_constant(table: st.IdentifierTable, name: str) -> bool:
    return is_declared(table, name) and \
        table.get_entry(table.search(name)).type == IdentifierType.CONSTANT


def get_constant_int_value(table: st.IdentifierTable, name: str) -> int:
    return table.get_entry(table.search(name)).value


def is_variable_declared(table: st.IdentifierTable, name: str) -> bool:
    if not is_declared(table, name):
        return False
    entry = table.get_entry(table.search(name))
    if entry.type != IdentifierType.VARIABLE:
        raise_error(SEMANTIC_ERROR,
                     f"l'identificateur doit être une variable: {name}")
        return False
    return True


def is_type_of_integer(table: st.IdentifierTable, name: str) -> bool:
    entry = table.get_entry(table.search(name))
    if entry.var_type != 0:
        raise_error(TYPE_ERROR, f"entier: {name}")
        return False
    return True
