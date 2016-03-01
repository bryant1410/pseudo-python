# int Int
# float Float
# boolean Boolean
# str String
# [2] List<Int>
# {2: 2.0} Dict<Int, Float>
# [] List
# {} Dict

from pseudo_python.errors import PseudoPythonTypeCheckError

V = '_' # we don't really typecheck or care for a lot of the arg types, so just use this
_ = ()

# we use lists instead of tuples, because it's easier this way
# for different methods in the same type env to reference and update the same signature
# that helps us with inherited methods: each one updates the type signature for the whole hierarchy

def serialize_type(l):
    if isinstance(l, str):
        return l
    else:
        return '%s[%s]' % (l[0], '\n'.join(map(serialize_type, l[1])))

def add(l, r):
    if l == 'Float' and r in ['Float', 'Int']  or r == 'Float' and l in ['Float', 'Int']:
        return [l, r, 'Float']
    elif l == 'Int' and r == 'Int':
        return [l, r, 'Int']
    elif l == 'String' and r == 'String':
        return [l, r, 'String']
    elif isinstance(l, tuple) and l[0] == 'List' and l == r:
        return [l, r, l]
    else:
        raise PseudoPythonTypeCheckError("wrong types for +: %s and %s" % (serialize_type(l), serialize_type(r)))

def sub(l, r):
    if l == 'Float' and r in ['Float', 'Int'] or r == 'Float' and l in ['Float', 'Int']:
        return [l, r, 'Float']
    elif l == 'Int' and r == 'Int':
        return [l, r, 'Int']
    else:
        raise PseudoPythonTypeCheckError("wrong types for -: %s and %s" % (serialize_type(l), serialize_type(r)))

def mul(l, r):
    if l == 'Float' and r in ['Float', 'Int'] or r == 'Float' and l in ['Float', 'Int']:
        return [l, r, 'Float']
    elif l == 'Int' and r == 'Int':
        return [l, r, 'Int']
    elif l == 'Int' and (isinstance(r, tuple) and r[0] == 'List' or r == 'String'): 
        return [l, r, r]
    elif r == 'Int' and (isinstance(l, tuple) and l[0] == 'List' or l == 'String'):
        return [l, r, l]
    else:
        raise PseudoPythonTypeCheckError("wrong types for *: %s and %s" % (serialize_type(l), serialize_type(r)))

def div(l, r):
    if l == 'Float' and r in ['Float', 'Int'] or r == 'Float' and l in ['Float', 'Int']:
        return [l, r, 'Float']
    elif l == 'Int' and r == 'Int':
        return [l, r, 'Int']
    raise PseudoPythonTypeCheckError("wrong types for /: %s and %s" % (serialize_type(l), serialize_type(r)))

# for template types as list, dict @t is the type of list arg and @k, @v of dict args
TYPED_API = {
    # methods
    'global': {
        'exit':  ['Int', 'Void'],
        'wat':   ['Int'],
        'to_string': ['Any', 'String']
    },

    'io': {
        'display':     ['*Any', 'Void'],
        'read':        ['String'],
        'read_file':   ['String', 'String'],
        'write_file':  ['String', 'String', 'Void']
    },

    'operators': {
        '+': add,
        '-': sub,
        '*': mul,
        '/': div
    },
    
    'List': {
        'push':       ['@t', 'Void'],
        'pop':        ['@t'],
        'insert':     ['@t', 'Void'],
        'insert_at':  ['@t', 'Int', 'Void']
    }
    # 'List#pop':        [_, '@t'],
    # 'List#insert':     [_, 'Null'],
    # 'List#remove':     [_, 'Null'],
    # 'List#remove_at':  [_, 'Null'],
    # 'List#length':     [_, 'Int'],
    # 'List#concat_one': [_, 'List<@t>'],
    # 'List#concat':     [_, 'List<@t>'],
    # 'List#[]':         [_, '@t'],
    # 'List#[]=':        [_, 'Null'],
    # 'List#slice':      [_, 'List<@t>'],

    # 'Dict#keys':       [_, 'List<@k>'],
    # 'Dict#values':     [_, 'List<@v>'],
}