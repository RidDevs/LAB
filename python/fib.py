def fibo(n, a=0, b=1):
        if n == 0:
            return
        fib = a + b
        print(fib)
        fibo(n - 1, b, fib)

print("enter the no. of terms")
x = int(input())

if x >= 1:
    print(0)
if x >= 2:
    print(1)
    
fibo(int(x - 2))
