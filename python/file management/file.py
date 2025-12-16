FILENAME = "books.txt"

# Add Book
def add_book():
    isbn = input("Enter ISBN: ")
    name = input("Enter Book Name: ")
    author = input("Enter Author Name: ")

    f = open(FILENAME, "a")
    f.write(isbn + "|" + name + "|" + author + "\n")
    f.close()

    print("Book added successfully!\n")


# Search Book
def search_book():
    try:
        f = open(FILENAME, "r")
    except:
        print("No books found!\n")
        return

    key = input("Enter ISBN / Name / Author to search: ").lower()
    found = False

    for line in f:
        isbn, name, author = line.strip().split("|")

        if (key in isbn.lower() or
            key in name.lower() or
            key in author.lower()):

            print("\nBook Found")
            print("ISBN   :", isbn)
            print("Name   :", name)
            print("Author :", author)
            found = True

    f.close()

    if not found:
        print("Book not found!\n")


# Menu
while True:
    print("---- Book Management ----")
    print("1. Add Book")
    print("2. Search Book")
    print("3. Exit")

    ch = input("Enter choice: ")

    if ch == "1":
        add_book()
    elif ch == "2":
        search_book()
    elif ch == "3":
        print("Exit")
        break
    else:
        print("Invalid choice\n")
