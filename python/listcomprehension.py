

numbers = [1, 2, 3, 4, 5]
squares = [x ** 2 for x in numbers if x % 2 != 0]  

print("Odd numbers:", [x for x in numbers if x % 2 != 0])

print("Squares of odd numbers:", squares)



