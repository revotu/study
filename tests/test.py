
import os


def random_string_1(n):
    return (''.join(map(lambda xx:(hex(ord(xx))[2:]), os.urandom(n))))[0:16]


def random_string_2(n):
    return (''.join([(hex(ord(xx))[2:]) for xx in os.urandom(n)]))[0:16]


print [(hex(ord(xx))[2:]) for xx in os.urandom(1)]
print random_string_1(1)
print random_string_2(1)
