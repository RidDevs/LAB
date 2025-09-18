number = int(input("Enter a number: "))
sum = 0
while number > 0:
    digit = number % 10     
    sum += digit 
    number //= 10           

print("Sum of digits =",sum)

