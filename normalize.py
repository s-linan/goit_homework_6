import re

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

def normalize(name: str) -> str:
    t_name = name.translate(TRANS)
    if '.' in t_name:
        split_t_name = t_name.split('.')
        suffix = '.' + split_t_name.pop()
        t_name = '.'.join(split_t_name)
        t_name = re.sub(r'\W', '_', t_name) + suffix
        print(t_name)
    else:
        t_name = re.sub(r'\W', '_', t_name)
    return t_name