__author__ = 'hone'

import copy

class A(object):
    def __init__(self, monkey, blue = []):
        self.monkey = monkey
        self.blue = blue

class B(object):
    def __init__(self, monkey, blue):
        self.monkey = monkey
        self.blue = blue

class C(A):
    def __init__(self, monkey, blue):
        self.monkey = monkey
        self.blue = blue

class D(A):
    pass

class E(object):
    def __init__(self, monkey):
        self.monkey = monkey

vars = [
    {"monkey": "tingo", "blue": []},
    {"monkey": "tango", "blue": []},
    {"monkey": "tongo", "blue": []},
    {"monkey": "bingo", "blue": ["x"]},
    {"monkey": "bango", "blue": ["y"]},
    {"monkey": "bongo", "blue": ["z"]},
    {"monkey": "jingo", "blue": ["a"]},
    {"monkey": "jango", "blue": ["b"]},
    {"monkey": "jongo", "blue": ["c"]},
]
classes = [A, B, C, D]

instances = []
# for c in classes:
#     for var in vars:
#         x = c(var['monkey'], var['blue'])
#         instances.append(x)

for c in classes:
    for var in vars:
        #nvar = copy.deepcopy(var)
        x = c(str(var['monkey']), list(var['blue']))
        instances.append(x)

for var in vars:
    x = E(var['monkey'])
    x.blue = var['blue']
    instances.append(x)

for var in vars:
    x = E(var['monkey'])
    x.blue = []
    instances.append(x)

count = 0
for i in instances:
    count += count
    name = type(i).__name__
    print name
    print i.monkey
    print i.blue
    i.blue.append(name)
    print i.blue

