# error.py

from global_state import get_num_ligne, get_carlu, get_unilex

EXCEED_LENGTH_IDENT = 2
EXCEED_LENGTH_STRING = 3
EXCEED_LENGTH_INT = 4
SYNTAXE_ERROR = 5
UNDECLARE_VARIABLE = 6
TYPE_ERROR = 7
SEMANTIC_ERROR = 8

_error_message = ""

class EndOfFile(Exception):
    def __str__(self):
        return "Fin du fichier Source"

def set_error_message(msg):
    global _error_message
    _error_message = msg

def get_error_message(error_number):
    if error_number == EXCEED_LENGTH_IDENT:
        return "L'identificateur dépasse la taille maximale"
    elif error_number == EXCEED_LENGTH_STRING:
        return "La chaîne de caractère dépasse la taille maximale"
    elif error_number == EXCEED_LENGTH_INT:
        return "Le nombre dépasse la taille maximale"
    elif error_number == SYNTAXE_ERROR:
        return f"Erreur syntaxtique dans une instruction {_error_message} attendu"
    elif error_number == UNDECLARE_VARIABLE:
        return f"Variable non déclarée: {_error_message}"
    elif error_number == TYPE_ERROR:
        return f"l'identificateur doit être de type {_error_message}"
    elif error_number == SEMANTIC_ERROR:
        return f"SEMANTIC ERROR: {_error_message}"
    else:
        return "Une erreur inconnue est survenue"

def raise_error(error_number):
    raise Exception(
        f"Error: {error_number} {get_error_message(error_number)}\n"
        f"In line: {get_num_ligne()} {get_carlu()} {get_unilex()}"
    )

def raise_end_of_file():
    raise EndOfFile()
