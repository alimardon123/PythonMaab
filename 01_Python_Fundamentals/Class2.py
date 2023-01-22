# 1.
# a = float(input("Enter the number: "))
# if a < 0:
#     a = a * -1
# print(f"Absolute of number is {a}")    

# 2.
# cur_year = int(input("Enter the current year: "))
# dob = int(input("Enter your year of birth: "))
# age = cur_year - dob
# if 18 <= age <= 28:
#     print(f"Your age is {age}. You are elegible.")
# else:
#     print(f"Your age is {age}. You are not elegible.")    

# 3.
# date = input("Enter a date in the following format:\n 6/18/99 (month/day/year)\n : ")
# d_numbers = (date.split("/"))
# m = int(d_numbers[0])
# d = int(d_numbers[1])
# y = int(d_numbers[2])
# if m * d == y:
#     print("Date is magic!")
# else:
#     print("Date is not magic!")    

# 4.
# a1 = float(input("Enter the length of First rectange: "))
# b1 = float(input("Enter the width of First rectange: "))
# a2 = float(input("Enter the length of Second rectange: "))
# b2 = float(input("Enter the width of Second rectange: "))
# s1 = a1 * b1
# s2 = a2 * b2
# if s1 > s2:
#     print("First rectangle has a greater area.")
# elif s1 < s2:
#     print("Second rectangle has a greater area.")
# if s1 == s2:
#     print("Areas of both rectangles are same!")

# 5.
a = int(input("Enter the starting number: "))
b = int(input("Enter the ending number: "))
if a % 2 != 0:
    a = a + 1
numbers = [*range(a, b+1, 2)]
print(len(numbers))
