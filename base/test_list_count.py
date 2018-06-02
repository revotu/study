from collections import Counter
import numpy as np

l = [1, 2, 1, 2, 3, 1, 2, 3, 3, 4, 5, 6, 7, 4, 8, 2, 2, 1, 1, 3]


def list_to_dict(l):
    d = {}
    for v in l:
        d[v] = l.count(v)
    return d


print(list_to_dict(l))


def collect(l):
    return dict(Counter(l))

print(collect(l))

print(dict(zip(*np.unique(l, return_counts=True))))

x, y = np.unique(l, return_counts=True)
print x
print y
print(type(x), type(y))