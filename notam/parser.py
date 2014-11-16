import ply.yacc as yacc
from . import lexer, ast, utils

tokens = lexer.tokens


# # # HELPER FUNCTIONS # # #

def _one_or_many(p):
    """
    This is used for tokens that may occur 1 or more times. The tokens are all
    packed into a list.
    """
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        SyntaxError('Invalid number of symbols')


# # # GRAMMAR DEFINITIONS # # #

def p_notam(p):
    """notam : intro attributes"""
    p[0] = ast.Notam(intro=p[1], attributes=p[2])


def p_intro(p):
    """intro : notam_id OPERATION
             | notam_id OPERATION notam_id"""
    if len(p) == 3:
        target = None
    elif len(p) == 4:
        target = p[3]
    else:
        SyntaxError('Invalid number of symbols')
    p[0] = ast.Intro(id=p[1], operation=p[2], target=target)


def p_notam_id(p):
    """notam_id : NOTAM"""
    parts = p[1].split('/')
    series = parts[0][0]
    number = int(parts[0][1:5])
    _year = int(parts[1])
    if _year >= 70:
        year = _year + 1900
    else:
        year = _year + 2000
    p[0] = ast.NotamID(series, number, year, raw=p[1])


def p_attributes(p):
    """attributes : attribute
                  | attribute attributes"""
    _one_or_many(p)


def p_attribute(p):
    """attribute : KEYWORD qualifiers
                 | KEYWORD LOCATION
                 | KEYWORD DATETIME
                 | KEYWORD schedule
                 | KEYWORD description"""
    p[0] = ast.Attribute(type=p[1], body=p[2])


def p_qualifiers(p):
    """qualifiers : QUALIFIER
                  | QUALIFIER qualifiers"""
    _one_or_many(p)


def p_schedule(p):
    """schedule : scheduleentry
                | scheduleentry schedule"""
    _one_or_many(p)


def p_scheduleentry(p):
    """scheduleentry : MONTHDAY TIME UNTIL TIME"""
    p[0] = p[1], p[2], p[3], p[4]


def p_description(p):
    """description : WORD
                   | WORD description"""
    _one_or_many(p)


def p_error(p):
    print('Syntax error in input at {!r}'.format(p))


# # # CREATE PARSER # # #

yacc.yacc()


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
        t = yacc.parse(source.read())

    # Print AST

    utils.print_ast(t)
