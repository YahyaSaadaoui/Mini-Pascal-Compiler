# constants.py

# Operation codes
ADDI = 0
SOUS = 1
MULTI = 2
DIV = 3
MOIN = 4
AFFE = 5
LIRE = 6
ECRL = 7
ECRE = 8
ECRC = 9
FINC = 10
EMPI = 11
CONT = 12
STOP = 13

OPERATION_NAMES = {
    ADDI: "ADDI",
    SOUS: "SOUS",
    MULTI: "MULT",
    DIV: "DIV",
    MOIN: "MOIN",
    AFFE: "AFFE",
    LIRE: "LIRE",
    ECRL: "ECRL",
    ECRE: "ECRE",
    ECRC: "ECRC",
    FINC: "FINC",
    EMPI: "EMPI",
    CONT: "CONT",
    STOP: "STOP"
}

def get_opcode_name(code):
    return OPERATION_NAMES.get(code)

def get_opcode_code(name):
    for k, v in OPERATION_NAMES.items():
        if v == name:
            return k
    return None


# Lexical units (tokens)
motcle = "motcle"
ident = "ident"
ent = "ent"
ch = "ch"
virg = "virg"
ptvirg = "ptvirg"
point = "point"
deuxpts = "deuxpts"
parouv = "parouv"
parfer = "parfer"
inf = "inf"
sup = "sup"
eg = "eg"
plus = "plus"
moins = "moins"
mult = "mult"
divi = "divi"
infe = "infe"
supe = "supe"
diff = "diff"
aff = "aff"

# Identifier types
VARIABLE = "VARIABLE"
CONSTANT = "CONSTANT"
FUNCTION = "FUNCTION"
PARAMETER = "PARAMETER"
