import AppOpener
import os
import re

from ply import lex, yacc

tokens = (
    'OPEN',
    'CLOSE',
    'PLAY',
    'APP',
    'WEBSITE',
    'VIDEO',
    'DIRECTORY',
    'FILE',
    'PATH',
    'NAME'
)

current_dir = ""
prev_dir = ""


def t_OPEN(t):
    r"""open"""
    return t


def t_CLOSE(t):
    r"""close"""
    return t


def t_PLAY(t):
    r"""play"""
    return t


def t_APP(t):
    r"""app"""
    return t


def t_WEBSITE(t):
    r"""website"""
    return t


def t_VIDEO(t):
    r"""video"""
    return t


def t_DIRECTORY(t):
    r"""directory"""
    return t


def t_FILE(t):
    r"""file"""
    return t


def t_NAME(t):
    r'\"(.+)*\"'
    return t


def t_PATH(t):
    r"""\b[a-zA-Z]:\\((\w+)|\\)*|prev(ious)?\b"""
    return t


def p_command(p):
    """
    command : OPEN action
            | CLOSE action
            | PLAY action
    """
    p[0] = (p[1], p[2])


def p_action(p):
    """
    action : APP NAME
           | WEBSITE NAME
           | VIDEO NAME
           | DIRECTORY PATH
           | FILE NAME
    """

    if not re.search(r'[a-z]:\\((\w+)|\\)*', p[2]):
        p[2] = p[2].replace('"', '')
    else:
        p[2] = p[2].upper()
    p[0] = (p[1], p[2])


def open_path(path):
    if re.search(r'[Pp]rev(ious)?', path):
        os.chdir(prev_dir)
    elif re.search(r'[a-z]:\\((\w+)|\\)*', path):
        os.chdir(path)
    else:
        print("path name does not exist")


def open_app(name):
    AppOpener.open(name)


def open_file(name):
    extensions = []


def close_app(name):
    AppOpener.close(name)


def process_input(input):
    if input[0] == "open":
        if input[1][0] == "app":
            open_app(input[1][1])
        elif input[1][0] == "directory":
            open_path(input[1][1])
        elif input[1][0] == "file":
            open_file(input[1][1])


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
        parsed_input = parser.parse(s)
        process_input(parsed_input)
    except EOFError:
        break
