x= int(input("Enter range start "))
y= int(input("Enter range end "))

sum=0
for i in range(x,y+1):
    if i%2==0: 
        sum+=i
print("Sum of even numbers from", x, "to", y, "is", sum)
