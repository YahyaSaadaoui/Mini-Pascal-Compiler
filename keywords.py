# keywords.py

from global_state import get_reserved_words

def is_keyword(word):
    return word.upper() in get_reserved_words()
