import tkinter as tk
from tkinter import messagebox

FILENAME = "book.txt"

#Add 
def add_book():
    isbn = entry_isbn.get()
    name = entry_name.get()
    author = entry_author.get()

    if isbn == "" or name == "" or author == "":
        messagebox.showwarning("Error", "All fields are required")
        return

    with open(FILENAME, "a") as f:
        f.write(isbn + "|" + name + "|" + author + "\n")

    messagebox.showinfo("Success", "Book added")

    entry_isbn.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_author.delete(0, tk.END)


#Search 
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
            result += line

    f.close()

    if result == "":
        messagebox.showinfo("Result", "No book found")
    else:
        messagebox.showinfo("Result", result)


#GUI 
root = tk.Tk()
root.title("Book System")
root.geometry("300x350")

tk.Label(root, text="Add Book").pack()

entry_isbn = tk.Entry(root)
entry_isbn.pack()
entry_isbn.insert(0, "ISBN")

entry_name = tk.Entry(root)
entry_name.pack()
entry_name.insert(0, "Book Name")

entry_author = tk.Entry(root)
entry_author.pack()
entry_author.insert(0, "Author")

tk.Button(root, text="Add", command=add_book).pack(pady=10)

tk.Label(root, text="Search Book").pack(pady=10)

entry_search = tk.Entry(root)
entry_search.pack()

tk.Button(root, text="Search", command=search_book).pack(pady=10)

root.mainloop()
