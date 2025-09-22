def checknum (num):
    if num % 2 == 0:
        return f"{num} is an even number"
    else:
        return f"{num} is an odd number"

num = int(input("input a number: "))
result=checknum(num)
print(result)

for i in range(1,6):
    print(i)

def multiplicationtable(num):
    print(f"multiplication table for {num}")
    for i in range(1,11):
        print(f"{num} x {i} = {num * i}")

num = int(input("input a number: "))
multiplicationtable(num)