import re

def is_numeric (word):
    m = re.search ('[0-9]', word)
    if m is None:
        return False
    return True
