source = None
carlu = None
running = True
unilex = None
nombre = None
chaine = None
num_ligne = 0
table_mots_reserve = []

NB_MOT_RESERVES = 8
LONG_MAX_INDENT = 20
LONG_MAX_CHAINE = 50
MAX_INT = 32767

nb_const_chaine = 0
val_de_const_chaine = []
derniere_adresse_var_glob = -1
error_message = ''


def get_source():
    return source


def set_source(value):
    global source
    source = value


def get_carlu():
    return carlu


def set_carlu(value):
    global carlu
    carlu = value


def get_unilex():
    return unilex


def set_unilex(value):
    global unilex
    unilex = value


def get_nombre():
    return nombre


def set_nombre(value):
    global nombre
    nombre = value


def get_chaine():
    return chaine


def set_chaine(value):
    global chaine
    chaine = value


def get_num_ligne():
    return num_ligne


def set_num_ligne(value):
    global num_ligne
    num_ligne = value


def get_table_mots_reserve():
    global table_mots_reserve
    if not table_mots_reserve:
        init_table_mots_reserve()
    return table_mots_reserve


def init_table_mots_reserve():
    global table_mots_reserve
    mots = ["PROGRAMME", "DEBUT", "FIN", "CONST", "VAR", "ECRIRE", "LIRE"]
    table_mots_reserve = sorted(mots)


def get_nb_const_chaine():
    return nb_const_chaine


def set_nb_const_chaine(value):
    global nb_const_chaine
    nb_const_chaine = value


def get_val_de_const_chaine():
    return val_de_const_chaine


def set_val_de_const_chaine(value):
    global val_de_const_chaine
    val_de_const_chaine = value


def get_derniere_adresse_var_glob():
    return derniere_adresse_var_glob


def increment_derniere_adresse_var_glob():
    global derniere_adresse_var_glob
    derniere_adresse_var_glob += 1


def get_error_message():
    return error_message


def set_error_message(value):
    global error_message
    error_message = value

_reserved_words = []

def init_reserved_words():
    global _reserved_words
    _reserved_words = [
        "PROGRAMME", "DEBUT", "FIN",
        "CONST", "VAR", "ECRIRE", "LIRE"
    ]

def get_reserved_words():
    if not _reserved_words:
        init_reserved_words()
    return _reserved_words