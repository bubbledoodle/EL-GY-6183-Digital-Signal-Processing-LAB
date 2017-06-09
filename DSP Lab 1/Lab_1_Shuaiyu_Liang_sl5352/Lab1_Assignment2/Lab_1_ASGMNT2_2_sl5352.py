import random
import my_sort_methods
import math
x = []
for i in range(0,9):
    x.append(math.floor(random.uniform(5,99)))
print "raw x: " + `x`
my_sort_methods.sort_2(x)
