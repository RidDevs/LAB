x = int(input("enter number: "))

if x < 2:
    print(x,"is not prime")
else:
    for i in range(2, int(x**0.5) + 1):
        if x % i == 0:
            print(x,"is not prime")
            break
    else:
        print(x," is prime")

