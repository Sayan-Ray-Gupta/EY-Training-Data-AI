import numpy as np

data = np.array([80,55,40,35])

print ("max Marks:", data.max())
print ("min Marks:", data.min())
print ("average:", data.mean())

mark = np.array([90,70,40,10,65])
print("first 3 element:", mark[:3])
print("reversed:", mark[::-1])
print("Sum", np.sum(mark))
print("standard deviation", np.std(mark))