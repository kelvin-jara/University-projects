"""
x = [1, 'a', 'X', 2, 'b', 'Y', 1, 'a', 'X', 1, 'a', 'X', 'd', 'd', 'z']
listLetters = []
dic = {}
for i in x:
    if isinstance(i, str) and i.islower():
        # print("str :", i, "capital or not:", i.islower())
        listLetters.append(i)


for i in listLetters:
    repetitions = 0
    for j in listLetters:
        if i == j:
            repetitions = repetitions + 1
    dic[i] = repetitions
"""
"""
Assume that you already have a variable called 'x', which contains a dictionary.

Modify 'x' with the dictionary y = {'c': 3, 'd': 3} in the following way:
- add to 'x' all key-value pairs of 'y' for which the key is not also present
in 'x'
- delete from 'x' all key-value pairs for which the key is also present in 'y'

For example:
If  then the value of x at the end of your program
should be equal to:
x = {'a': 1, 'b': 2, 'd': 3}
"""
""""
y = {'c': 3, 'd': 3, 'j': 3}
x = {'a': 1, 'b': 2, 'c': 3, 'd': 3}
z = {}
for i in x:
    if i not in y.keys():
        z[i] = x[i]

for i in y:
    if i not in x.keys():
        z[i] = y[i]
print(z)
x = [16, 14, 9, 10, 20]
print(len(x))
"""
namesS = []
namesB = []
buyers = {'buyer1': [19, 16, 12], 'buyer2': [16, 14, 10], 'buyer3': [16, 14, 9], 'buyer4': [20, 14, 12]}
sellers = {'seller1': [10, 11, 16], 'seller2': [13, 15, 16], 'seller3': [15, 17, 20], 'seller4': [9, 14, 15]}
buyers = {'buyer1': [16, 15, 13], 'buyer2': [15, 8, 5], 'buyer3': [11, 10, 9], 'buyer4': [16, 6, 5]}
sellers = {'seller1': [8, 13, 14], 'seller2': [6, 10, 16], 'seller3': [6, 8, 9], 'seller4': [7, 9, 11]}
transactions = 0
sell = []
buy = []
for i, j in zip(buyers, sellers):
    for k in range(3):
        buy.append(buyers[i][k])
        sell.append(sellers[j][k])

sell.sort()
buy.sort(reverse=True)
for i, j in zip(buy, sell):
    if i >= j:
        transactions = transactions + 1
print(buy, "\n", sell, "\n", transactions)


