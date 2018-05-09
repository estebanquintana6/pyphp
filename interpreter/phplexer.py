import ply.lex as lex


reserved = ('IF', 'ELSE', 'FOR', 'VAR', 'BOOL', 'FUNCTION')

nonparsed = ('WHITESPACE', 'COMMENT', 'START', 'END')

tokens = reserved + nonparsed + (
    'ID',
    'NUMBER',
    'STRING',
    'STARTCLOSE',
    'PLUS',
    'MINUS',
    'MUL',
    'DIV',
    'NOT',
    'AND',
    'OR',
    'XOR',
    'COMP',
    'EQ',
    'GREATER',
    'LESS',
    'GREATER_OR_EQUAL',
    'SMALLER_OR_EQUAL',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'SCOLO',
    'COMMA'
)

t_STRING = r'"(.*?)"'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_NOT = r'!='
t_AND = r'&'
t_OR = r'\|'
t_COMP = r'=='
t_EQ = r'='
t_GREATER = r'>'
t_LESS = r'<'
t_SMALLER_OR_EQUAL = r'<='
t_GREATER_OR_EQUAL = r'>='
t_XOR = r'\^'
t_COMMA = r','

t_LPAREN = r'\('
t_RPAREN = r'\)'

t_SCOLO = r';'

t_LBRACKET = r'\{'
t_RBRACKET = r'\}'


def t_FUNCTION(t):
    r'function'
    return t


def t_IF(t):
    r'if'
    return t


def t_ELSE(t):
    r'else'
    return t


def t_BOOL(t):
    r'true|false'
    return t


def t_VAR(t):
    r'var'
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t


def t_NUMBER(t):
    r'(0b[01]+)|(0x[0-9A-Fa-f]+)|\d+'
    t.value = int(t.value)
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def t_WHITESPACE(t):
    r'[ \t\r\n]+'
    t.lexer.skip(0)


def t_COMMENT(t):
    r'\/\*(\*(?!\/)|[^*])*\*\/'
    t.lexer.skip(0)

def t_START(t):
    r'\<\?php'
    t.lexer.skip(0)


def t_END(t):
    r'\?>'
    t.lexer.skip(0)


lex.lex()


with open('example.php', 'r') as file:
    s = file.read()
lex.input(s)
while True:
    tok = lex.token()
    if not tok:
        break  # No more input
    print(tok)
