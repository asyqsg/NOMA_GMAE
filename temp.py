import numpy as np


a = np.array([[1,2,3],[4,5,3]])
b = []
for i in range(len(a)):
    temp = np.argmax(a[i])
    print(temp)
print(b)
print(type(a))
print(a.shape)