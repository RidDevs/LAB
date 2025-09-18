gen=0
prev=0
curr=1
print(prev)
print(curr)
for gen in range(18):
    fib= prev + curr
    print(fib)
    prev= curr
    curr= fib
    gen+=1
