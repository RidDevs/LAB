import tkinter as tk
from tkinter import messagebox

FILENAME = "books.txt"

# ------------------ Functions ------------------

def add_book():
    isbn = entry_isbn.get().strip()
    name = entry_name.get().strip()
    author = entry_author.get().strip()

    if not isbn or not name or not author:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    try:
        with open(FILENAME, "a") as f:
            f.write(f"{isbn}|{name}|{author}|Yes\n")
        messagebox.showinfo("Success", "Book added successfully!")

        entry_isbn.delete(0, tk.END)
        entry_name.delete(0, tk.END)
        entry_author.delete(0, tk.END)

    except:
        messagebox.showerror("Error", "Could not write to file!")


def search_book():
    key = entry_search.get().strip().lower()
    if not key:
        messagebox.showwarning("Input Error", "Enter some search text!")
        return

    try:
        f = open(FILENAME, "r")
    except FileNotFoundError:
        messagebox.showerror("Error", "books.txt not found!")
        return

    found = []
    for line in f:
        parts = line.strip().split("|")
        if len(parts) != 4:
            continue
        isbn, name, author, available = parts

        if key in isbn.lower() or key in name.lower() or key in author.lower():
            found.append(line.strip())

    f.close()

    if found:
        messagebox.showinfo("Results", "\n".join(found))
    else:
        messagebox.showinfo("Not Found", "No matching book found.")


def modify_book():
    isbn_find = entry_mod_isbn.get().strip()
    if not isbn_find:
        messagebox.showwarning("Error", "Enter ISBN to modify!")
        return

    try:
        f = open(FILENAME, "r")
    except FileNotFoundError:
        messagebox.showerror("Error", "books.txt not found!")
        return

    books = []
    updated = False

    for line in f:
        parts = line.strip().split("|")
        if len(parts) != 4:
            continue

        isbn, name, author, available = parts

        if isbn == isbn_find:
            name = entry_mod_name.get().strip() or name
            author = entry_mod_author.get().strip() or author
            available = entry_mod_avail.get().strip() or available
            updated = True

        books.append(f"{isbn}|{name}|{author}|{available}\n")

    f.close()

    if updated:
        with open(FILENAME, "w") as f:
            f.writelines(books)
        messagebox.showinfo("Success", "Book updated successfully!")
    else:
        messagebox.showinfo("Not Found", "No book found with that ISBN!")
        


# ------------------ GUI ------------------

root = tk.Tk()
root.title("Book Management System")
root.geometry("350x450")

tk.Label(root, text="Add Book", font=("Arial", 12, "bold")).pack()
tk.Label(root, text="ISBN:").pack()
entry_isbn = tk.Entry(root, width=30)
entry_isbn.pack()

tk.Label(root, text="Name:").pack()
entry_name = tk.Entry(root, width=30)
entry_name.pack()

tk.Label(root, text="Author:").pack()
entry_author = tk.Entry(root, width=30)
entry_author.pack()

tk.Button(root, text="Add Book", command=add_book).pack(pady=10)


# ----- Search Section -----
tk.Label(root, text="Search Book", font=("Arial", 12, "bold")).pack(pady=5)
tk.Label(root, text="Enter ISBN/Name/Author:").pack()

entry_search = tk.Entry(root, width=30)
entry_search.pack()

tk.Button(root, text="Search", command=search_book).pack(pady=10)


# ----- Modify Section -----
tk.Label(root, text="Modify Book", font=("Arial", 12, "bold")).pack()

tk.Label(root, text="ISBN to Modify:").pack()
entry_mod_isbn = tk.Entry(root, width=30)
entry_mod_isbn.pack()

tk.Label(root, text="New Name:").pack()
entry_mod_name = tk.Entry(root, width=30)
entry_mod_name.pack()

tk.Label(root, text="New Author:").pack()
entry_mod_author = tk.Entry(root, width=30)
entry_mod_author.pack()

tk.Label(root, text="Available (Yes/No):").pack()
entry_mod_avail = tk.Entry(root, width=30)
entry_mod_avail.pack()

tk.Button(root, text="Modify", command=modify_book).pack(pady=10)

root.mainloop()
