__author__ = 'Montya'

import numpy as np

a = np.zeros((5,), dtype=np.int)


a[0] = a[0] + 1
a[2] = a[2] + 5

index = a.argmax();
print(index)
print (a)