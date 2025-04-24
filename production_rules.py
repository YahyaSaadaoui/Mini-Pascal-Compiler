# production_rules.py
"""
Functional port of semanticAnalyzer.ProductionRules.java

The parser/semantic-checker drives:
    • lexer.py        – supplies next tokens (updates global_state.Global)
    • semantic.py     – symbol-table + semantic checks
    • codegen.py      – emits P-code

No classes, no OOP: everything is pure functions manipulating a single
`ctx` dict that carries the collaborating components created in main.
"""

from global_state import Global as G
from constants import LexicalUnit as LU
from error import raise_error, SYNTAXE_ERROR, SEMANTIC_ERROR
from codegen import (
    new_intermediate_code,
    new_code_generator,
)
from semantic import new_table_semantic_analyser

# ────────────────────────────── context helpers ─────────────────────────────
def new_context(lexer, identifier_table):
    """Build the working context (parser state)."""
    intermediate = new_intermediate_code()
    table_analyser = new_table_semantic_analyser(identifier_table)
    codegen = new_code_generator(intermediate, table_analyser)

    return {
        "lexer": lexer,
        "table": table_analyser,
        "intermediate": intermediate,
        "codegen": codegen,
    }


def advance(ctx):
    """Fetch next token, updating Global.unilex."""
    G.setUnilex(ctx["lexer"].analex())


# ───────────────────────────── dispatch / driver ────────────────────────────
def dispatch(ctx) -> bool:
    """Top-level router – mimics the big switch in Java."""
    ul = G.getUnilex()
    lexeme = G.getChaine()

    # keyword-led rules
    if ul == LU.motcle:
        return any(
            rule(ctx)
            for kw, rule in {
                "PROGRAMME": prog,
                "CONST": decl_const,
                "VAR": decl_var,
                "DEBUT": bloc,
                "LIRE": lecture,
                "ECRIRE": ecriture,
            }.items()
            if kw == lexeme
        )

    # identifier-led rules
    if ul == LU.ident:
        return affectation(ctx)

    # expression pieces
    if ul in (LU.ent, LU.ch):
        return exp(ctx)

    if ul in (LU.plus, LU.moins, LU.mult, LU.divi):
        return op_bin(ctx)

    return False


# ───────────────────────────── grammar procedures ───────────────────────────
def expect(ctx, token, err_msg):
    """Utility to consume *token* or raise syntax error."""
    if G.getUnilex() != token:
        raise_error(SYNTAXE_ERROR, err_msg)
    advance(ctx)


def prog(ctx):
    expect(ctx, LU.motcle, "programme, mot clé PROGRAMME")
    expect(ctx, LU.ident, "programme, identificateur")
    expect(ctx, LU.ptvirg, "programme, ';'")
    print("Prog")
    return True


def decl_const(ctx):
    if not (G.getUnilex() == LU.motcle and G.getChaine() == "CONST"):
        return False

    advance(ctx)  # skip CONST

    var_names, uls, values = [], [], []

    while True:
        if G.getUnilex() != LU.ident:
            raise_error(SEMANTIC_ERROR, "const, identificateur")
        var_names.append(G.getChaine())
        advance(ctx)

        expect(ctx, LU.eg, "const, '='")

        if G.getUnilex() not in (LU.ent, LU.ch):
            raise_error(SYNTAXE_ERROR, "const, entier ou chaine")
        uls.append(G.getUnilex())
        values.append(G.getNombre())
        advance(ctx)

        if G.getUnilex() != LU.virg:
            break
        advance(ctx)

    expect(ctx, LU.ptvirg, "const, ';'")

    for v, ul, val in zip(var_names, uls, values):
        if not ctx["table"].define_constant(v, ul, val):
            return False

    print("DeclConst")
    return True


def decl_var(ctx):
    if not (G.getUnilex() == LU.motcle and G.getChaine() == "VAR"):
        return False
    advance(ctx)  # skip VAR

    names = []
    while True:
        if G.getUnilex() != LU.ident:
            raise_error(SYNTAXE_ERROR, "var, identificateur")
        names.append(G.getChaine())
        advance(ctx)
        if G.getUnilex() != LU.virg:
            break
        advance(ctx)

    expect(ctx, LU.ptvirg, "var, ';'")

    for n in names:
        if not ctx["table"].define_variable(n):
            return False
    print("DeclVar")
    return True


def bloc(ctx):
    if not (G.getUnilex() == LU.motcle and G.getChaine() == "DEBUT"):
        raise_error(SYNTAXE_ERROR, "bloc, mot clé DEBUT")
    advance(ctx)
    print("Debut Bloc")

    if not instruction(ctx):
        raise_error(SYNTAXE_ERROR, "bloc, instruction")

    while G.getUnilex() == LU.ptvirg:
        advance(ctx)
        instruction(ctx)

    if not (G.getUnilex() == LU.motcle and G.getChaine() == "FIN"):
        raise_error(SYNTAXE_ERROR, "bloc, mot clé FIN")
    advance(ctx)
    print("Fin Bloc")
    return True


def instruction(ctx):
    ul, lexeme = G.getUnilex(), G.getChaine()
    if ul == LU.ident:
        return affectation(ctx)
    if ul == LU.motcle and lexeme in ("LIRE", "ECRIRE", "DEBUT"):
        return {"LIRE": lecture, "ECRIRE": ecriture, "DEBUT": bloc}[lexeme](ctx)
    return False


def affectation(ctx):
    if G.getUnilex() != LU.ident:
        raise_error(SYNTAXE_ERROR, "affectation, identificateur")
    var_name = G.getChaine()
    advance(ctx)

    if not ctx["table"].is_variable_declared(var_name):
        return False

    expect(ctx, LU.aff, "affectation, ':='")

    if not exp(ctx):
        raise_error(SYNTAXE_ERROR, "affectation, expression")

    ctx["codegen"].gen_code_affectation(var_name)
    print("Affectation")
    return True


def lecture(ctx):
    if not (G.getUnilex() == LU.motcle and G.getChaine() == "LIRE"):
        raise_error(SYNTAXE_ERROR, "lecture, mot clé LIRE")
    advance(ctx)

    expect(ctx, LU.parouv, "lecture, '('")

    while True:
        if G.getUnilex() != LU.ident:
            raise_error(SYNTAXE_ERROR, "lecture, identificateur")
        name = G.getChaine()
        if not ctx["table"].is_variable_declared(name):
            return False
        ctx["codegen"].gen_code_read(name)
        advance(ctx)
        if G.getUnilex() != LU.virg:
            break
        advance(ctx)

    expect(ctx, LU.parfer, "lecture, ')'")

    print("Lecture")
    return True


def ecriture(ctx):
    if not (G.getUnilex() == LU.motcle and G.getChaine() == "ECRIRE"):
        raise_error(SYNTAXE_ERROR, "ecriture, mot clé ECRIRE")
    advance(ctx)

    expect(ctx, LU.parouv, "ecriture, '('")

    first = True
    while True:
        if first:
            first = False
        else:
            advance(ctx)
        if G.getUnilex() == LU.ch:
            ctx["codegen"].gen_code_ecr_exp_string()
            advance(ctx)
        elif exp(ctx):
            ctx["codegen"].gen_code_ecr_exp()
        else:
            break
        if G.getUnilex() != LU.virg:
            break

    expect(ctx, LU.parfer, "ecriture, ')'")

    print("Ecriture")
    return True


# ───────────────────────────── expression parsing ───────────────────────────
def exp(ctx):
    if not terme(ctx):
        return False
    advance(ctx)
    if suite_terme(ctx):
        ctx["codegen"].gen_code_exp()
        return True
    return False


def suite_terme(ctx):
    if op_bin(ctx):
        advance(ctx)
        return exp(ctx)
    return True


def op_bin(ctx):
    ctx["codegen"].gen_code_op_bin()
    return G.getUnilex() in (LU.plus, LU.moins, LU.mult, LU.divi)


def terme(ctx):
    ul = G.getUnilex()
    if ul == LU.ent:
        ctx["codegen"].gen_code_terme_int()
        return True
    if ul == LU.ident and ctx["table"].is_declared(G.getChaine()) and ctx["table"].is_type_of_integer(G.getChaine()):
        ctx["codegen"].gen_code_terme_ident()
        return True
    if ul == LU.parouv:
        advance(ctx)
        ok = exp(ctx) and G.getUnilex() == LU.parfer
        return ok
    if ul == LU.moins:
        advance(ctx)
        if terme(ctx):
            ctx["codegen"].gen_code_terme_minus()
            return True
    return False
