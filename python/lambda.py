
square = lambda x: x ** 2  

numbers = [1, 2, 3, 4, 5]
squared = list(map(square, numbers)) 

print("Original numbers:", numbers)
print("Squared numbers:", squared)
