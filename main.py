from ply import lex, yacc
import os
import AppOpener
import re

tokens = (
    'COMMAND',
    'ARGUMENT',
    'PATH',
)

current_dir = ""
prev_dir = ""


def t_COMMAND(t):
    r"""\b[Gg][Dd]|[Oo]pen\b"""
    return t


def t_PATH(t):
    r"""\b[A-Z]:\\((\w+)|\\)*|[Pp]rev(ious)?\b"""
    return t


def p_command(p):
    """command : COMMAND PATH"""
    if re.search(r'[Gg][Dd]', p[1]):
        if re.search(r'[Pp]rev(ious)?', p[2]):
            os.chdir(prev_dir)
        elif re.search(r'[A-Z]:\\((\w+)|\\)*', p[2]):
            os.chdir(p[2])
    else:
        print("Unknown command")


def t_error(t):
    print(f"Illegal character {t.value[0]}")
    t.lexer.skip(1)


def p_error(p):
    print("Syntax error")


t_ignore = ' \t'

lexer = lex.lex()
parser = yacc.yacc()

while True:
    try:
        prev_dir = current_dir
        current_dir = os.getcwd()
        s = input(f"{current_dir}>")
        parser.parse(s)
    except EOFError:
        break
