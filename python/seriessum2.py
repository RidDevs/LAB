print("series:  (x^2)/(x+2) + (x^2)/(x+3) + x(x^2)/(x+4) + ... + (x^2)/(x+n)")
print()
x = int(input("enter x- "))
n = int(input("enter n(number of terms in the series)- "))

sum = 0
for i in range(2, n + 1):
    sum += (x ** 2) / (x + i)

print("Sum =", sum)