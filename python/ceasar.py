#ceasear is cypher

text = "the brown fox went over the lazy dog"

letters = "abcdefghijklmnopqrstuvwxyz"
shift_amount = 3  
result = ""

for char in text:
    if char in letters:
        pos = letters.find(char)
        new_pos = (pos + shift_amount) % 26
        result += letters[new_pos]
    else:
        result += char
        
print(result)
    
