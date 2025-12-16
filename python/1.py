import tkinter as tk
from tkinter import messagebox

FILENAME = "books.txt"

# ---------- Add Book ----------
def add_book():
    isbn = entry_isbn.get()
    name = entry_name.get()
    author = entry_author.get()

    if isbn == "" or name == "" or author == "":
        messagebox.showwarning("Error", "All fields required")
        return

    f = open(FILENAME, "a")
    f.write(isbn + "|" + name + "|" + author + "\n")
    f.close()

    messagebox.showinfo("Success", "Book Added")

    entry_isbn.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_author.delete(0, tk.END)


# ---------- Search Book ----------
def search_book():
    key = entry_search.get().lower()

    if key == "":
        messagebox.showwarning("Error", "Enter search text")
        return

    try:
        f = open(FILENAME, "r")
    except:
        messagebox.showerror("Error", "File not found")
        return

    result = ""
    for line in f:
        if key in line.lower():
            result = result + line

    f.close()

    if result == "":
        messagebox.showinfo("Result", "No book found")
    else:
        messagebox.showinfo("Result", result)


# ---------- GUI ----------
root = tk.Tk()
root.title("Book Management")
root.geometry("300x350")

tk.Label(root, text="Add Book, Enter ISBN | NAME | AUTHOR").pack()

entry_isbn = tk.Entry(root)
entry_isbn.pack()

entry_name = tk.Entry(root)
entry_name.pack()

entry_author = tk.Entry(root)
entry_author.pack()

tk.Button(root, text="Add Book", command=add_book).pack(pady=10)

tk.Label(root, text="Search Book").pack()

entry_search = tk.Entry(root)
entry_search.pack()

tk.Button(root, text="Search", command=search_book).pack(pady=10)

root.mainloop()
