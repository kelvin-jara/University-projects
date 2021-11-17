import numpy as np
import  math
import pandas as pd


"""
#x = [[0,0, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]]
x = [[1,0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, 1]]
x = [[1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0]]
x = np.array(x)
l = x.reshape(1, -1)
print(l)
colums = 8
rows = 2
xloc, yloc = [], []
for i, v in enumerate(l[0]):
    if v == 1:
        x, y = i%colums , math.floor(i/colums)
        xloc.append(x), yloc.append(y)
print(xloc, "\n", yloc)
"""

"""
x = [1, 2, 3, 4]
lasti = -1
for i, v in enumerate(x):
    print(i - lasti)
    lasti = i
print(x)
"""


