import ply.yacc as yacc
import phplexer as lexer


errors = []

class Node:
    def __init__(self, token, value=None, ntype=None, children=None):
            self.token = token
            self.value = value
            self.ntype = ntype
            if children:
                self.children = children
            else:
                self.children = []

    def get_values(self):
        return '"' + self.token + ':' + str(self.value) + ':' + \
                str(self.ntype) + '"'

    def debug(self):

        if self.children:
            for child in self.children:
                print(self.get_values(), '->', child.get_values())
                child.debug()


class Stack:
    def __init__(self, list):
        self.list = list

    def push(self, tup):
        self.list.append(tup)

    def pop(self):
        self.list.pop()

    def delete(self, name):
        self.list.remove(name)

    def find(self, name):
        for item in self.list:
            if item.variable == name:
                return item
        return -1


class StackRow:
    def __init__(self, variable='', value='None', type='None'):
        self.variable = variable
        self.value = value
        self.type = type

    def to_string(self):
        return str('name: ' + self.variable + ' value: ' + repr(self.value) + ' type: '+ self.type)


tokens = lexer.tokens


precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'COMP'),
    ('nonassoc', 'EQ', 'GREATER', 'LESS'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV'),
    ('right', 'NOT'),
    ('right', 'LBRACKET'),
    # ('left', 'ELSEIF'),
    # ('left', 'ELSE'),
)


# Catastrophic error handler
def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error somewhere unknown")


def p_program(p):
    """
    program : declaration-list
    """
    p[0] = Node("program", None, None, [p[1]])
    p[0].debug()
    print("\n")

def p_declarationlist(p):
    """
    declaration-list : declaration
                   | declaration declaration-list
    """
    if len(p) == 2:
        p[0] = Node("declaration-list", None, None, [p[1]])
    else:
        p[0] = Node("declaration-list", None, None, [p[1], p[2]])


def p_declaration(p):
    """
    declaration : funDeclaration
                | varDeclaration
    """
    p[0] = Node("declaration", None, None, [p[1]])


def p_varDeclaration(p):
    """
    varDeclaration : VAR ID SCOLO
                    | VAR ID EQ expression SCOLO
    """
    if len(p) == 6:
        p[0] = Node('varDeclaration', [p[2], p[2]], None, None)
    else:
        p[0] = Node('varDeclaration', [p[2]], None, None)


def p_funDeclaration(p):
    """
    funDeclaration : FUNCTION function
    """
    T = Node("FUNCTION")
    p[0] = Node("function-declaration", None, None, [T, p[2]])


def p_function(p):
    """
    function : ID parameters block
    """
    T = Node("ID", p[1])
    p[0] = Node("function", None, None, [T, p[2], p[3]])


def p_parameters(p):
    """
    parameters : LPAREN RPAREN
               | LPAREN paramList RPAREN
    """
    T1 = Node("LPAREN", p[1])
    if (len(p) == 3):  # First case
        T2 = Node("RPAREN", p[2])
        p[0] = Node("parameters", None, None, [T1, T2])
    else:
        T2 = Node("RPAREN", p[3])
        p[0] = Node("parameters", None, None, [T1, T2, p[2]])


def p_parameter_list(p):
    """
    paramList : parameter
                   | parameter COMMA paramList
    """
    if len(p) == 2:
        p[0] = Node('parameter-list', None, None, [p[1]])
    else:
        T = Node('COMMA', p[2])
        p[0] = Node('parameter-list', None, None, [p[1], T, p[3]])


def p_parameter(p):
    """
    parameter : ID
    """
    T = Node('ID', p[1])
    p[0] = Node('parameter', None, None, [T])


def p_block(p):
    """
    block : LBRACKET RBRACKET
          | LBRACKET statement-list RBRACKET
    """
    T1 = Node("LBRACKET", p[1])

    if (len(p) == 3):  # First case
        T2 = Node("RBRACKET", p[2])
        p[0] = Node("block", None, None, [T1, T2])
    else:
        T2 = Node("RBRACKET", p[3])
        p[0] = Node("block", None, None, [T1, T2, p[2]])


def p_statement_list(p):
    """
    statement-list : statement
                   | statement statement-list
    """
    if len(p) == 2:
        p[0] = Node('statement-list', None, None, [p[1]])
    else:
        p[0] = Node('statement-list', None, None, [p[1], p[2]])


def p_statement(p):
    """
    statement : declaration
              | expression
              | if-statement
    """
    p[0] = Node('statement', None, None, [p[1]])


def p_expression(p):
    """
    expression : basic-expr
    |
                | assignment-expr SCOLO
                | comparison-expr
    """
    p[0] = Node('expression', None, None, [p[1]])


def p_constant(p):
    """
    constant : NUMBER
             | STRING
    """
    v = Node('CONSTANT', p[1])
    p[0] = Node('constant', None, None, [v])

def p_basic(p):
    """
    basic-expr : ID
                | NUMBER
                | STRING
    """
    v = Node('BASIC', p[1])
    p[0] = Node('basic-expr', None, None, [v])


def p_id(p):
    """
    identifier : ID
                | NUMBER
    """
    T = Node('ID', p[1])
    p[0] = Node('identifier', None, None, [T])


def p_constant_assignation(p):
    """
    constant-assignation : identifier EQ constant
    """
    variable = StackRow()
    assign = Node('=', p[2])
    p[0] = Node('variable assignation', p[4].value, p[4].type, [p[1], assign, p[4]])
    name = ''

    for i in range(len(p[1].children)):
        name += p[1].children[i].value

    variable.variable = name
    variable.type = p[3].type

    if variableStack.find(name) == -1:
        if(variable.value is None or variable.type is None):
            errors.append("variable" + variable.variable + " has a declaration error")
        else:
            variableStack.push(variable)
    else:
        temp = variableStack.find(name)
        temp.value = p[3].value
        temp.type = p[3].type

def p_assignment_expression(p):
    """
    assignment-expr : identifier  math-operator basic-expr
                     | identifier math-operator assignment-expr
    """
    if len(p) == 4:
        p[0] = Node('assignment-expr', None, None, [p[1], p[2], p[3]])
    else:
        p[0] = Node('assignment-expr', None, None, [p[1]])


def p_comparison_expr(p):
    """
    comparison-expr : basic-expr comp-operator basic-expr
                          | basic-expr comp-operator comparison-expr
    """
    p[0] = Node('comparison-expr', None, None, [p[1], p[2], p[3]])


def p_comparison_operators(p):
    """
    comp-operator : GREATER
                    | LESS
                    | GREATER_OR_EQUAL
                    | SMALLER_OR_EQUAL
                    | COMP
                    | NOT
    """
    T = Node(p[1], p[1])
    p[0] = Node('comp-operator', None, None, [T])


def p_varAssignation(p):
    """
    varAssignation : ID EQ constant SCOLO
    """
    variable = StackRow()
    assign = Node('=', p[2])
    p[0] = Node('variable assignation', p[4].value, p[4].type, [p[1], assign, p[4]])
    name = ''

    for i in range(len(p[1].children)):
        name += p[1].children[i].value

    variable.variable = name
    variable.type = p[3].type

    if variableStack.find(name) == -1:
        if(variable.value is None or variable.type is None):
            errors.append("variable" + variable.variable + " has a declaration error")
        else:
            variableStack.push(variable)
    else:
        temp = variableStack.find(name)
        temp.value = p[3].value
        temp.type = p[3].type

def p_binary_op(p):
    """
    math-operator : PLUS
                | MINUS
                | MUL
                | DIV
                | EQ
    """
    T = Node(p[1], p[1])
    p[0] = Node('bin_op', None, None, [T])


def p_if_statement(p):
    """
    if-statement : IF LPAREN expression RPAREN block
                | IF LPAREN expression RPAREN block ELSE else-statement
    """

    if len(p) == 6:
        T = Node('IF', p[1])
        p[0] = Node('if-statement', None, None, [T, p[3], p[5]])
    else:
        T1 = Node('IF', p[1])
        T2 = Node('ELSE', p[4])
        p[0] = Node('if-else-statement', None, None, [T1, p[3], p[5], T2, p[7]])


def p_else_statement(p):
    """
    else-statement : block
    """
    p[0] = Node('else-statement', None, None, [p[1]])


variableStack = Stack([])
parser = yacc.yacc(debug=True)

with open('example.php', 'r') as file:
    s = file.read()
    parser.parse(s)