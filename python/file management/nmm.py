FILENAME = "books.txt"


# Add 

def add_book():
    isbn = input("Enter ISBN: ")
    name = input("Enter Book Name: ")
    author = input("Enter Author Name: ")

    with open(FILENAME, "a") as f:
        f.write(isbn + "|" + name + "|" + author + "\n")

    print("\nBook added!\n")


# Search 


def search_book():
    try:
        f = open(FILENAME, "r")
    except:
        print("\nNo books found!\n")
        return

    search_value = input("Enter ISBN/Name/Author to search: ").lower()
    found = False

    for line in f:
        parts = line.strip().split("|")

        # Handle both 3-field & 4-field formats
        if len(parts) == 3:
            isbn, name, author = parts
            available = "Unknown"
        elif len(parts) == 4:
            isbn, name, author, available = parts
        else:
            continue

        if (search_value in isbn.lower() or
            search_value in name.lower() or
            search_value in author.lower()):

            print("\n--- Book Found ---")
            print("ISBN:", isbn)
            print("Name:", name)
            print("Author:", author)
            print("Available:", available)
            found = True

    f.close()

    if not found:
        print("\nNo matching book found!\n")


# Modify 

def modify_book():
    try:
        f = open(FILENAME, "r")
    except:
        print("\nNo books found!\n")
        return

    isbn_to_change = input("Enter ISBN of book to modify: ")
    books = []
    updated = False

    for line in f:
        isbn, name, author = line.strip().split("|")

        if isbn == isbn_to_change:
            print("\nCurrent Book Details:")
            print("Name:", name)
            print("Author:", author)

            name = input("Enter new Book Name: ")
            author = input("Enter new Author Name: ")
            updated = True

        books.append(isbn + "|" + name + "|" + author + "\n")

    f.close()

    if updated:
        with open(FILENAME, "w") as f:
            f.writelines(books)
        print("\nBook updated!\n")
    else:
        print("\nBook not found!\n")


# Menu

def menu():
    while True:
        print("----- Book Management System -----")
        print("1. Add Book")
        print("2. Search Book")
        print("3. Modify Book")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            search_book()
        elif choice == "3":
            modify_book()
        elif choice == "4":
            print("\nExiting...")
            break
        else:
            print("\nInvalid choice!\n")

menu()
