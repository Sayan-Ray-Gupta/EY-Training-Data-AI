set_a = {"Rahul", "priya", "max"}
set_b = {"Rahul", "priya", "amit"}

#print(set_a | set_b) #union
#print(set_a & set_b) #intersection
#print(set_a - set_b) #difference
#print(set_b - set_a)


set_c = {"Rahul", "priya", "amit", "priya","max", "Rahul"}
unique_names = set(set_c)
print(unique_names)