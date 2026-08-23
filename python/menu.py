print("Series generator menu")
print("1. fibonacci")
print("2. even number series")
print("3. square number series")

series = int(input("enter choice: "))
if series>0 and series<4:
    x = int(input("how many terms to generate? "))

if series == 1:
    a = 0
    b = 1
    for i in range(x):
        print(a)
        c = a + b
        a = b
        b = c

elif series == 2:
    for i in range(2, 2*x + 1, 2):
        print(i)

elif series == 3:
    for i in range(1, x + 1):
        print(i * i)

else:
    print("Invalid Choice")