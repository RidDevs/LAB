var = "original"

def show():
    global var
    print(var)
    var = "modified"
    print(var)
    
show()
print(var)