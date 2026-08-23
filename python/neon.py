x = int(input("enter number: "))

square = x * x
sum = 0

while square > 0:
    sum += square % 10
    square //= 10

if sum == x:
    print(x,"is neon number")
else:
    print(x,"is not a neon number")