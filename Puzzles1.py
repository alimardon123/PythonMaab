# 1.
input = "python.class"
print(input[:input.find(".")])

# 2.
numbers = []
for n in range(1, 1001):
    if n % 7 == 0 and n % 5 !=0:
        numbers.append(n)
print(numbers)      