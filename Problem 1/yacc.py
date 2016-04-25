import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lex import tokens

DEBUG = True

# Namespace & built-in functions

name = {}
let_d = {} # Dictionary that stores variable name and value ( Example: {'a' : 3} )
terms = [] # Keeps track of the terms in order to match dictionary variables to their values

def cons(l):
    return [l[0]] + l[1]

name['cons'] = cons

def concat(l):
    return l[0] + l[1]

name['concat'] = concat

def listar(l):
    return l

name['list'] = listar

def car(l):
    return l[0][0]

name['car'] = car

def cdr(l):
    return l[0][1:]

name['cdr'] = cdr

def eq(l):
    return l[0] == l[1]

name['eq'] = eq
name['='] = eq

def _and(l):
    return not False in l

name['and'] = _and

def _or(l):
    return True in l

name['or'] = _or

def cond(l):
    if l[0]:
        return l[1]

name['cond'] = cond

def add(l):
    global terms
    terms = list(l) # Copy list "l" to the "terms" list
    return sum(l)

name['+'] = add

def minus(l):
    '''Unary minus'''
    return -l[0]

name['-'] = minus

def _print(l):
    print lisp_str(l[0])

name['print'] = _print

def let(l):
    # (let (a 3) (+ 1 a))
        # Calling a with [3]
        # Calling + with [1, 'a']
        # Calling let with [['a', 3], <function add at 0x2>]
    let_d[l[0][0]] = l[0][1] # Add the variable and its value to the dictionary
    #result = lisp_eval(l[1][0], [l[1][1], let_d[l[0][0]]])
    #result = name[l[1][0]](l[1][1], let_d[l[0][0]])
    #result = call(name[l[1][0]], [1, let_d[l[0][0]]])
    #result = l[1]([let_d[l[0][0]], 1])
    variable_index = terms.index(l[0][0]) # Index of variable
    terms[variable_index] = let_d[l[0][0]] # Replace the variable letter with the actual value
    result = l[1](terms) # Calculate the final result
    del let_d[l[0][0]] # Delete the variable from the dictionary
    return result

name['let'] = let

def _if(l):
    # Format: (if #t 1 2) - if true, return 1; otherwise, return 2
        # l[0] = #t, l[1] = 1, l[2] = 2
    if l[0] == True:
        return l[1]
    else:
        return l[2]

name['if'] = _if

#  Evaluation functions

def lisp_eval(simb, items):
    if simb in name:
        return call(name[simb], eval_lists(items))
    else:
       return [simb] + items

def call(f, l):
    try:
        return f(eval_lists(l))  
    except TypeError:
        return f

def eval_lists(l):
    r = []
    for i in l:
        if is_list(i):
            if i:
                r.append(lisp_eval(i[0], i[1:]))
            else:
                r.append(i)
        else:
            r.append(i)
    return r

# Utilities functions

def is_list(l):
    return type(l) == type([])

def lisp_str(l):
    if type(l) == type([]):
        if not l:
            return "()"
        r = "("
        for i in l[:-1]:
            r += lisp_str(i) + " "
        r += lisp_str(l[-1]) + ")"
        return r
    elif l is True:
        return "#t"
    elif l is False:
        return "#f"
    elif l is None:
        return 'nil'
    else:
        return str(l)

# BNF

def p_exp_atom(p):
    'exp : atom'
    p[0] = p[1]

def p_exp_qlist(p):
    'exp : quoted_list'
    p[0] = p[1]

def p_exp_call(p):
    'exp : call'
    p[0] = p[1]

def p_quoted_list(p):
    'quoted_list : QUOTE list'
    p[0] = p[2]

def p_list(p):
    'list : LPAREN items RPAREN'
    p[0] = p[2]

def p_items(p):
    'items : item items'
    p[0] = [p[1]] + p[2]

def p_items_empty(p):
    'items : empty'
    p[0] = []

def p_empty(p):
    'empty :'
    pass

def p_item_atom(p):
    'item : atom'
    p[0] = p[1]

def p_item_list(p):
    'item : list'
    p[0] = p[1]

def p_item_list(p):
    'item : quoted_list'
    p[0] = p[1]
        
def p_item_call(p):
    'item : call'
    p[0] = p[1]

def p_item_empty(p):
    'item : empty'
    p[0] = p[1]

def p_call(p):
    'call : LPAREN SIMB items RPAREN'
    if DEBUG: print "Calling", p[2], "with", p[3]
    p[0] = lisp_eval(p[2], p[3])

def p_atom_simbol(p):
    'atom : SIMB'
    p[0] = p[1]

def p_atom_bool(p):
    'atom : bool'
    p[0] = p[1]

def p_atom_num(p):
    'atom : NUM'
    p[0] = p[1]

def p_atom_word(p):
    'atom : TEXT'
    p[0] = p[1]

def p_atom_empty(p): 
    'atom :'
    pass

def p_true(p):
    'bool : TRUE'
    p[0] = True

def p_false(p):
    'bool : FALSE'
    p[0] = False

def p_nil(p):
    'atom : NIL'
    p[0] = None

# Error rule for syntax errors
def p_error(p):
    print "Syntax error!! ",p

# Build the parser
# Use this if you want to build the parser using SLR instead of LALR
# yacc.yacc(method="SLR")
yacc.yacc()


