FILENAME = "books.txt"

def add_book():
    isbn = input("Enter ISBN: ")
    name = input("Enter Book Name: ")
    author = input("Enter Author Name: ")
    available = "Yes"

    with open(FILENAME, "a") as f:
        f.write(f"{isbn}|{name}|{author}|{available}\n")

    print("\nBook added successfully!\n")


def search_book():
    try:
        f = open(FILENAME, "r")
    except FileNotFoundError:
        print("\nNo records found! (books.txt not created yet)\n")
        return

    print("\nSearch by:")
    print("1. ISBN")
    print("2. Book Name")
    print("3. Author")
    choice = input("Enter choice: ")

    key = ""
    if choice == "1":
        key = "isbn"
    elif choice == "2":
        key = "name"
    elif choice == "3":
        key = "author"
    else:
        print("Invalid choice!\n")
        return

    value = input("Enter search value: ").lower()
    found = False

    for line in f:
        # Split safely
        parts = line.strip().split("|")
        if len(parts) != 4:
            continue  # skip bad lines

        isbn, name, author, available = parts

        if (key == "isbn" and isbn == value) or \
           (key == "name" and name.lower() == value) or \
           (key == "author" and author.lower() == value):

            print("\n--- Book Found ---")
            print("ISBN:", isbn)
            print("Name:", name)
            print("Author:", author)
            print("Available:", available)
            found = True

    f.close()

    if not found:
        print("\nNo book found!\n")


def modify_book():
    try:
        f = open(FILENAME, "r")
    except FileNotFoundError:
        print("\nNo records found! (books.txt not created yet)\n")
        return

    isbn_search = input("Enter ISBN of the book to modify: ")

    updated = False
    books = []

    for line in f:
        parts = line.strip().split("|")
        if len(parts) != 4:
            continue  # skip invalid lines

        isbn, name, author, available = parts

        if isbn == isbn_search:
            print("\nCurrent Details:")
            print(f"{isbn} | {name} | {author} | {available}")

            name = input("Enter new Book Name: ")
            author = input("Enter new Author Name: ")
            available = input("Is the book available? (Yes/No): ")

            updated = True

        books.append(f"{isbn}|{name}|{author}|{available}\n")

    f.close()

    if updated:
        with open(FILENAME, "w") as f:
            f.writelines(books)
        print("\nBook details updated!\n")
    else:
        print("\nBook with this ISBN not found!\n")


def menu():
    while True:
        print("-------- Book Management System --------")
        print("1. Add New Book")
        print("2. Search Book")
        print("3. Modify Book")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            search_book()
        elif choice == "3":
            modify_book()
        elif choice == "4":
            print("Exiting Program...")
            break
        else:
            print("Invalid choice! Try again.\n")


menu()
