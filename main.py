import sys
import webbrowser
import AppOpener
import os
import re

from youtubesearchpython import VideosSearch
from googlesearch import search
from ply import lex, yacc

tokens = (
    'ACTION',
    'TYPE',
    'SYS',
    'NAME',
    'PATH'
)

current_dir = ""
prev_dir = ""


def t_ACTION(t):
    r"""open|close|play"""
    return t


def t_TYPE(t):
    r"""app|(video|movie|song)|website|dir|file"""
    return t


def t_SYS(t):
    r"""exit|clear|list"""
    return t


def t_NAME(t):
    r'\"(.+)*\"'
    return t


def t_PATH(t):
    r"""\b[a-zA-Z]:\\((\w+)|\\)*|prev(ious)?\b"""
    return t


def p_command(p):
    """
    command : ACTION type
    """
    p[0] = (p[1], p[2])


def p_type(p):
    """
    type :  TYPE NAME
        |   TYPE PATH
    """

    if not re.search(r'[a-zA-Z]:\\((\w+)|\\)*', p[2]):
        p[2] = p[2].replace('"', '')
    else:
        p[2] = p[2].upper()
    p[0] = (p[1], p[2])


def p_sys(p):
    """command : SYS"""
    p[0] = (p[1])


def console_clear():
    os.system('cls')


def open_path(path):
    if re.search(r'[Pp]rev(ious)?', path):
        os.chdir(prev_dir)
    elif re.search(r'[a-zA-Z]:\\((\w+)|\\)*', path):
        os.chdir(path)
    else:
        print("path name does not exist")


def open_app(name):
    AppOpener.open(name)


def open_file(name):
    files = os.listdir(os.getcwd())
    for file in files:
        if re.search(name, file):
            print(f"opening {file}...")
            os.startfile(name)
        else:
            print("file not found, check name or directory")


def open_website(name):
    search_results = [x for x in search(name, num=5, stop=5)]

    print("Here are 5 first query results")
    for i in range(0, 5):
        print(f"{i+1}. {search_results[i]}")
    choice = int(input("Choose website: "))

    webbrowser.open(search_results[choice-1])


def close_app(name):
    AppOpener.close(name)


def play_video(name):
    fetched_data = VideosSearch(name, limit=5)

    print("Here are 5 first query results")
    for i in range(0, 5):
        print(f'{i+1}. {fetched_data.result()["result"][i]["title"]}')
    choice = int(input("Choose website: "))

    webbrowser.open(fetched_data.result()["result"][choice-1]["link"])


def process_input(input_tokens):
    try:
        if input_tokens[0] == "open":
            if input_tokens[1][0] == "app":
                open_app(input_tokens[1][1])
            elif input_tokens[1][0] == "dir":
                open_path(input_tokens[1][1])
            elif input_tokens[1][0] == "file":
                open_file(input_tokens[1][1])
            elif input_tokens[1][0] == "website":
                open_website(input_tokens[1][1])
        elif input_tokens[0] == "close":
            if input_tokens[1][0] == "app":
                close_app(input_tokens[1][1])
        elif input_tokens[0] == "play":
            if re.search(r'(video|movie|song)', input_tokens[1][0]):
                play_video(input_tokens[1][1])
        elif input_tokens == "exit":
            sys.exit()
        elif input_tokens == "list":
            for file in os.listdir(os.getcwd()):
                print(file)
        elif input_tokens == "clear":
            console_clear()
    except TypeError:
        print("Command unrecognized")


def t_error(t):
    # print(f"Illegal character {t.value[0]}")
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
        s = input(f"{current_dir}>").strip().lower()
        parsed_input = parser.parse(s)
        process_input(parsed_input)
    except EOFError:
        break
