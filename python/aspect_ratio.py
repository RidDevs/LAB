def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def aspect_ratio(width, height):
    divisor = gcd(width, height)
    return width // divisor, height // divisor



resolution = input("Enter resolution (width<space>height): ").split()
width, height = map(int, resolution)
ratio = aspect_ratio(width, height)
print(f"Aspect ratio: {ratio[0]}:{ratio[1]}")
