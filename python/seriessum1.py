print("series:   x/(2^2) + 2x/(2^4) + 3x/(2^6) + ... + nx/2^(2n)")
print()
x = int(input("enter value of x- "))
n = int(input("enter value of n(number of terms in the series)- "))

sum = 0
for i in range(1, n + 1):
    sum += (i * x) / (2 ** (2 * i))

print("Sum =", sum)