
import os
from functools import reduce
from functools import partial as curry

COMMANDS = ["l", "r", "u", "d"]
DEFAULT_HEIGH = 30
DEFAULT_WIDTH = 30
DEFAULT_CONTENT = '*'
EMPTY = " "
CLEAR = "clear"
QUIT = "q"

class Node:
    def __init__( self, data ):
        self.content = data
        self.up      = self.down = None
        self.next    = self.prev = None

    def is_empty( self ):
        return self.content == EMPTY

    def swallow( self, node ):
        if self.is_empty():
            self.content = node.content

    def clean( self ):
        self.content = EMPTY

    @classmethod
    def create_default( klass ):
        return klass( DEFAULT_CONTENT )

    @classmethod
    def mkMutiple( self, times, data='*' ):
        return [Node(data) for _ in range(times)]

    def get_components( self ):
        try:
            components =  [
                self,           self.next,
                self.down,      self.down.next,
                self.down.down, self.down.down.next
            ]
            return components
        except Exception:
            return  []
    __repr__ = lambda self: self.content

def L():
    a, b, c, d = Node.mkMutiple(4)
    a.down = b
    b.down = c
    c.next = d
    return a

def T():
    a, b, c, d = Node.mkMutiple(4)
    a.down = b
    b.down = c
    b.next = d
    return a

def B():
    a, b, c, d = Node.mkMutiple(4)
    a.next = b
    c.next = d
    d.up   = b
    c.up   = a
    return a

def B():
    a, b, c, d = Node.mkMutiple(4)
    a.next = b
    c.next = d
    a.down = c
    b.down = d
    return a

def Z():
    a, b, c, d, e = Node.mkMutiple(5)
    a.down = b
    b.next = c
    c.down = d
    b.down = e
    return a




# Here is a generic moving object constructor
# Fully connected 

# Rotation as the composition of the transposition function
# and the reverse function


def generic_brik():
    def groupby( size, items ):
        if items == []:
            return []
        elif len( items ) is 1:
            return [items]
        brink = 0
        def capture( k, s ):
            brink = k
            return s
        return [
            [capture( k, s ) for (k, s) in enumerate( items ) if k < size]
        ] + groupby( size, items[brink + size:] )

    nodes = NodesGrid(1, 6).makeGrid().nodes.pop()
    v = groupby(2, NodesGrid(1, 6).nodes.pop())
    s = NodesGrid(3, 2)
    s.nodes = v
    return s.makeGrid().nodes.pop()

def extract( a ):
    q = n = a
    z = []
    while n is not None:
        q = n
        s = []
        while q:
            s.append( q.content )
            q = q.next
        z.append( s )
        if n.down is None:
            if n.next is not None:
                n = n.next.down
            else:
                n = None
        else:
            n = n.down
    return z

def padd( lst ):
    z = max( list(map(len, lst)) )
    for item in lst:
        size = z - len( item )
        item += [' '] * size
    return lst

def to_s( obj ):
    items = padd( extract( obj ) )
    return '\n'.join( [''.join( item ) for item in items ] )

class NodesGrid:
    def __init__( self, hight, width, rep=' ' ):
        self.hight = hight
        self.width = width
        self.nodes = None
        self.rep   = rep
        self.cursor = [0, hight // 2]
        self.r_idx  = 0
        self.makeGrid()

    def transpose( self ):
        return [
            [line[i] for line in self.nodes]
            for i, _ in enumerate(self.nodes[0])
        ]

    def map_( self, fn, items ):
        return list(map(fn, items))


    def makeGrid( self ):
        self.nodes = [
            [Node(self.rep) for i in range(self.width)]
            for j in range(self.hight)
        ]

        def vertical_bridge( n, n_ ):
            n.down = n_
            n_.up = n
            return n_

        def horizontal_bridge( node_1, node_2 ):
            node_1.next = node_2
            node_2.prev = node_1
            return node_2

        nodes = self.transpose()
        self.map_(curry(reduce, horizontal_bridge), self.nodes)
        self.map_(curry(reduce, vertical_bridge), nodes)
        return self


    def reset_cursor( self ):
        self.cursor = [0, self.hight // 2]

    def __str__( self ):
        q = ""
        for line in self.nodes:
            for node in line:
                q += node.content
            q += "\n"
        return ("-" * self.hight ) + "\n" + q + ("-" * self.hight)

    def intro_obj( self, obj ):
        i, j = self.cursor
        self.nodes[i][j].swallow( obj )


    def _rotate_obj_( self, obj ):
        #
        # * -> *
        # |    |
        # * -> * ==>  * -> * -> *
        # |    |      |    |    |
        # * -> *      * -> * -> *
        items = obj.get_components()


    def _move_obj_to_left( self, obj ):
        idx = self.cursor[1] - 1
        if idx < 0: return
        if self.nodes[self.cursor[0]][idx].content != EMPTY:
            return
        self.nodes[self.cursor[0]][self.cursor[1]].clean()
        self.cursor[1] -= 1

        i, j = self.cursor
        self.nodes[i][j].swallow( obj )

    def _move_obj_to_right( self, obj ):
        idx = self.cursor[1] + 1
        if idx >= len(self.nodes): return
        if self.nodes[self.cursor[0]][idx].content != EMPTY:
            return
        self.nodes[self.cursor[0]][self.cursor[1]].clean()
        self.cursor[1] += 1

        i, j = self.cursor
        self.nodes[i][j].swallow( obj )

    def _move_obj_up( self, obj ):
        if self.cursor[0] - 1 < 0:
            return
        self.nodes[self.cursor[0]][self.cursor[1]].clean()
        self.cursor[0] -= 1

        i, j = self.cursor
        self.nodes[i][j].swallow( obj )

    def _move_obj_down( self, obj ):
        idx = self.cursor[1] + 1
        if idx >= len(self.nodes) - 1: return
        if self.nodes[self.cursor[0]][idx].content != EMPTY:
            return

        self.nodes[self.cursor[0]][self.cursor[1]].clean()
        self.cursor[0] = self.cursor[0] + 1
        i, j = self.cursor
        self.nodes[i][j].swallow( obj )

    def has_reached_limit( self ):
        return self.cursor[0] == len( self.nodes ) - 1

    def is_valid_command( self, wanna_be_command ):
        return wanna_be_command in COMMANDS

    @classmethod
    def repl( klass ):
        instance = klass( DEFAULT_HEIGH, DEFAULT_WIDTH )

        # Commands dispatch mechanism

        TABLE = dict(zip(COMMANDS, [
            instance._move_obj_to_left,
            instance._move_obj_to_right,
            instance._move_obj_up,
            instance._move_obj_down
        ]))
        while True:
            obj = Node.create_default()
            while True:
                instance.intro_obj( obj )
                print( instance )
                choice = input(":").lower()
                if instance.has_reached_limit():
                    instance.reset_cursor()
                    break
                elif instance.is_valid_command( choice ):
                    TABLE[choice]( obj )
                elif choice == QUIT : break
                os.system( CLEAR )

