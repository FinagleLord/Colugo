# Just some ansi escape codes as variables to save space in main.py
class fg():
    "Text Color, add capital B before the colors name to make it bright"
    black    = '\u001b[30m' 
    red      = '\u001b[31m'
    green    = '\u001b[32m'
    yellow   = '\u001b[33m'
    blue     = '\u001b[34m'
    magenta  = '\u001b[35m'
    cyan     = '\u001b[36m'
    white    = '\u001b[37m'

    Bblack   = '\u001b[30;1m'
    Bred     = '\u001b[31;1m'
    Bgreen   = '\u001b[32;1m'
    Byellow  = '\u001b[33;1m'
    Bblue    = '\u001b[34;1m'
    Bmagenta = '\u001b[35;1m'
    Bcyan    = '\u001b[36;1m'
    Bwhite   = '\u001b[37;1m'
class bg():
    "Highlight Color, add capital B before the colors name to make it bright"
    black    = '\u001b[40m'
    red      = '\u001b[41m'
    green    = '\u001b[42m'
    yellow   = '\u001b[43m'
    blue     = '\u001b[44m'
    magenta  = '\u001b[45m'
    cyan     = '\u001b[46m'
    white    = '\u001b[47m'


    Bblack   = '\u001b[40;1m'
    Bred     = '\u001b[41;1m'
    Bgreen   = '\u001b[42;1m'
    Byellow  = '\u001b[43;1m'
    Bblue    = '\u001b[44;1m'
    Bmagenta = '\u001b[45;1m'
    Bcyan    = '\u001b[46;1m'
    Bwhite   = '\u001b[47;1m'

# SAME THING
reset      = '\u001b[0m'
clear      = '\u001b[0m'


def clp(string_to_print='', fgcolor='', bgcolor='', endcolor=reset):
    "print() with ansi coloring"
    return print(f'{fgcolor}{bgcolor}{string_to_print}{endcolor}')


def clo(string_to_print='', fgcolor='', bgcolor='', endcolor=reset):
    "str() with ansi coloring"
    return str(f'{fgcolor}{bgcolor}{string_to_print}{endcolor}')









