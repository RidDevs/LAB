import random

names = ["A", "B", "C", "D", "E", "F"]
no = len(names)

for i in range(no - 1, 0, -1):
    j = random.randint(0, i)  
   
    names[i], names[j] = names[j], names[i]

print("Shuffled list:", names)
