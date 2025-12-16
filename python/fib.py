def fib(n,a=0,b=1):
        
        if n == 0:
            return
        fibo = a + b
        print(fibo)
        fib(n - 1, b, fibo)

print("enter the no. of terms")
x = int(input())

if x >= 1:
    print(0)
if x >= 2:
    print(1)
    
fib(x - 2)