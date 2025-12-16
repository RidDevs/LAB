import random

secret = random.randint(1, 100)
count = 0

while True:
    guess = int(input("Enter your guess (1-100): "))
    count += 1

    if guess > secret:
        print("Too high! Try a smaller number.")
    elif guess < secret:
        print("Too low! Try a bigger number.")
    else:
        print("Correct! You guessed the number.")
        print("Number of tries:", count)
        break
