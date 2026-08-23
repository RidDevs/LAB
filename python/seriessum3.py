print("series:   x - x^2 + x^3 - x^4 + ... + x^n")
print() 

x = int(input("enter x- "))
n = int(input("enter n(number of terms in the series)- "))

sum = 0

for i in range(1, n + 1):
    if i % 2 == 0:
        sum -= x ** i
    else:
        sum += x ** i

print("Sum =", sum)