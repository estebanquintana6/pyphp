from compiler import ast

def less_compare((left, right)):
    return ast.Compare(left, [('<', right), ])


def greater_compare((left, right)):
    return ast.Compare(left, [('>', right), ])


def equals_compare((left, right)):
    return ast.Compare(left, [('==', right), ])


def greater_equal_compare((left, right)):
    return ast.Compare(left, [('>=', right), ])


def less_equal_compare((left, right)):
    return ast.Compare(left, [('<=', right), ])


def not_compare((left, right)):
    return ast.Compare(left, [('!=', right), ])


binary_ops = {
    '+': ast.Add,
    '-': ast.Sub,
    '*': ast.Mul,
    '/': ast.Div,
}

boolean_ops = {
    '|': ast.Or,
    '&': ast.And,
    '^': ast.Bitxor,
}

compare_ops = {
    '!=': not_compare,
    '<': less_compare,
    '<=': less_equal_compare,
    '==': equals_compare,
    '>': greater_compare,
    '>=': greater_equal_compare,
}

unary_ops = {
    "+": ast.UnaryAdd,
    "-": ast.UnarySub,
}

bool_ops = {
    '&&': ast.And,
    '||': ast.Or,
}


def Assign(left, right):
    names = []
    if isinstance(left, ast.Name):
        # Single assignment on left
        return ast.Assign([ast.AssName(left.name, 'OP_ASSIGN')], right)
    elif isinstance(left, ast.Tuple):
        # List of things - make sure they are Name nodes
        names = []
        for child in left.getChildren():
            if not isinstance(child, ast.Name):
                raise SyntaxError("that assignment not supported")
            names.append(child.name)
        ass_list = [ast.AssName(name, 'OP_ASSIGN') for name in names]
        return ast.Assign([ast.AssTuple(ass_list)], right)
    else:
        raise SyntaxError("Can't do that yet")