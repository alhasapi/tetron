







import inspect
from operator import not_
from functools import reduce
from pprint import pprint as p
from functools import partial as curry

def transpose( nodes ):
    return [
        [line[i] for line in nodes]
        for i, _ in enumerate(nodes[0])
    ]

def reverse(items):
    return list(reversed(items))

def compose(*fn):
    if len(fn) is 0:
        raise Exception("I expect at least one argument")

 #  if any(not isinstance(f, transpose.__class__) for f in fn):
 #      items = [str(type(f)) for f in fn if type(f) not in [transpose.__class__, print.__class__]]
 #      raise Exception(f"All arguments of must be functions not {' or '.join(items)}")

    if len(fn) is 1:
        return fn[0]

    atomiq = lambda f, g: lambda s: f(g(s))

    if len(fn) is 2:
        return atomiq(*fn)
    return reduce(atomiq, fn)

def w(n):
    t = [reverse, transpose]
    v, f = [], True
    for i in range(n):
        v.append(t[f])
        f = not f
    return v

def rotate(obj, rotation_state=3):
    def w2(n):
        return [
            reduce(compose,
                [not_ for i in range(i)]
            )(0) for i in range(1, n)
        ]
    items = map(
        lambda idx: [reverse, transpose][ idx ],
        w2( 4 )[ rotation_state ]
    )
    return reduce(
               compose,
               list( items )
        )( obj )

v = ['*', ' ', ' ']
s = ['*', '*', '*']
r = [' ', '*', ' ']
L = [v,v,s]
B = [s,s,s]
T = [s,r,r]
P = [v,v,v]
Z = [s,r,s]

def render(obj):
    print('\n'.join(map(lambda s: reduce(lambda x, y: x + y, s), obj)))

def tate(o):
    def _(idx):
        if idx > 4:
            raise SyntaxError("The maximum index is 4")
        return [compose(*w(i))(o) for i in range(1, 6)][ idx ]
    return _

def new_grid(grid_size=(10, 10)):
    hight, width = grid_size
    return [[' ' for i in range(hight)] for j in range(width)]

def padd( obj, grid_size=(10, 10) ):
    h, w  = grid_size
    lsize = h - len( obj[0] )

    wanna_be_added = [' ' for i in range( lsize )]

    def ol(line):
        return [' ' for i in range(4)] + line + [' ' for (i, _) in enumerate( line )]

    hight, width = grid_size
    obj_ = list(map(ol, obj))
    return [[' ' for i in range(hight)] for j in range(width - len(obj_))] + obj_


def merge( grid, obj ):
    def predicate():
        for (i, _) in enumerate( grid ):
            for item in grid[i]:
                pass

def zipWith(fn, a, b):
    return [fn(*items) for items in zip(a, b)]

def zipWith2(fn, *b):
    fn_arg_size = inspect.getargspec(fn).args.__len__()
    if fn_arg_size != len(b):
        raise Exception('Mismatch arguments list size')
    return [fn(*items) for items in zip(*b)]

def fn(a, b):
    v = []
    for (i, j) in zip(a, b):
        if i == j and i == ' ':
            v.append(i)
        elif i == '*':
            v.append(j)
        else:
            v.append(' ')
    return fn
