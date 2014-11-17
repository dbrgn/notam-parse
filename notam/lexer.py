import sys
import datetime

import ply.lex as lex
from ply.lex import TOKEN


# # # STATES # # #

states = (
    ('qualifiers', 'exclusive'),
    ('location', 'exclusive'),
    ('validity', 'exclusive'),
    ('description', 'exclusive'),
    ('limits', 'exclusive'),
    ('attributes', 'exclusive'),
)

# # # TOKEN LIST # # #

tokens = (
    # Common tokens
    'KEYWORD',
    'NOTAM', 'OPERATION',
    'DATETIME', 'WORD',
    # Qualifier tokens
    'QUALIFIER', 'COORDINATES',
    # Location tokens
    'LOCATION',
    # Validity tokens
    'MONTHDAY', 'TIME', 'UNTIL',
)


# # # TOKEN RULES # # #

# Regexes

re_year = r'[12][0-9]{3}'
re_monthday = r'[0-3][0-9]'
re_time = r'[0-2][0-9][0-6][0-9]'


# Common rules

def t_NOTAM(t):
    r'[A-Z][0-9]+/[0-9]{2}'
    return t


def t_KEYWORD(t):
    r'CREATED:|SOURCE:|[QABCDEFG]\)'
    if t.value.endswith(')'):
        letter = t.value[0]
        if letter == 'Q':
            t.lexer.begin('qualifiers')
        elif letter == 'A':
            t.lexer.begin('location')
        elif letter in ['B', 'C', 'D']:
            t.lexer.begin('validity')
        elif letter == 'E':
            t.lexer.begin('description')
        elif letter in ['F', 'G']:
            t.lexer.begin('limits')
    elif t.value.endswith(':'):
        t.lexer.begin('attributes')
    return t


def t_OPERATION(t):
    r'NOTAM[NRC]'
    types = {
        'N': 'NEW',
        'R': 'REPLACE',
        'C': 'CANCEL',
    }
    t.value = types[t.value[5]]
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')


t_ignore = ' \t\n'


# Qualifier rules (Q)

t_qualifiers_KEYWORD = t_KEYWORD
t_qualifiers_QUALIFIER = r'[A-Z0-9]+'
t_qualifiers_COORDINATES = r'[0-9]{,5}[NS][0-9]{,5}[EW][0-9]{,3}'
t_qualifiers_ignore = t_ignore + '/'


# Location rules (A)

t_location_KEYWORD = t_KEYWORD
t_location_LOCATION = r'[A-Z]+'
t_location_ignore = t_ignore


# Period of validity rules (B/C/D)

t_validity_KEYWORD = t_KEYWORD
t_validity_UNTIL = r'-'
t_validity_ignore = t_ignore


def t_validity_DATETIME(t):
    r'[0-9]{2}[01][0-9][0-3][0-9][02][0-9][0-6][0-9]'
    t.value = datetime.datetime.strptime(t.value, '%y%m%d%H%M')
    return t


@TOKEN(re_time)
def t_validity_TIME(t):
    return t


@TOKEN(re_monthday)
def t_validity_MONTHDAY(t):
    return t


# Description rules (E)

t_description_KEYWORD = t_KEYWORD
t_description_WORD = '[^ \n]+'
t_description_ignore = t_ignore


# Limit rules (F/G)

t_limits_KEYWORD = t_KEYWORD
t_limits_ignore = t_ignore


# Attribute rules

t_attributes_KEYWORD = t_KEYWORD
t_attributes_WORD = '[^ \n]+'
t_attributes_ignore = t_ignore


def t_attributes_DATETIME(t):
    r'[0-3][0-9]\s[A-Z][a-z]{2}\s[12][0-9]{3}\s[0-9]{2}:[0-9]{2}:[0-9]{2}'
    t.value = datetime.datetime.strptime(t.value, '%d %b %Y %H:%M:%S')
    return t


# # # CREATE LEXER # # #

lex.lex()


# # # PROCESS INPUT # # #

if __name__ == '__main__':

    # Get file as argument

    import sys
    if len(sys.argv) != 2:
        print('You need to specify a NOTAM source file to read from.', file=sys.stderr)
        sys.exit(1)
    if not sys.argv[1].endswith('.txt'):
        print('Argument needs to be a .txt file.', file=sys.stderr)
        sys.exit(1)

    sourcefile = sys.argv[1]

    # Read source file

    with open(sourcefile, 'r') as source:
        lex.input(source.read())

    # Read tokens

    state = ''
    while True:
        token = lex.token()
        if token is None:
            break
        new_state = lex.lexer.current_state()
        if new_state != state:
            state = new_state
            print('\n[%s]' % state)
        print(token)
