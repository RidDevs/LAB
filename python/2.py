import tkinter as tk
from tkinter import messagebox

FILENAME ="test.txt"

def add():
    isbn = entry_isbn.get()
    book = entry_book.get()
    author = entry_author.get()

    f= open(FILENAME,"a")
    f.write(isbn+"|"+book+"|"+author+"\n")
    f.close()

    messagebox.showinfo("Added")

    entry_isbn.delete(0,tk.END)
    entry_book.delete(0,tk.END)
    entry_author.delete(0,tk.END)

def search():
    key = entry_search.get()
    f = open(FILENAME,"a")
    f = open(FILENAME,"r")
    result=""
    for line in f:
        if key in line:
            result = result + line
    f.close

    if result == "":
        print("not found")
    else: 
        messagebox.showinfo("found ISBN | bookname | author ", result)
    entry_search.delete(0,tk.END)

def modify():

    isbn= entry_isbn2.get()
    book= entry_book2.get()
    author= entry_author2.get()
    f= open(FILENAME,"a")
    f = open(FILENAME,"r")
    found=0
    lines=[]
    for line in f:
        parts=line.strip().split("|")

        if parts[0]==isbn:
            found=1
            parts[1]=book
            parts[2]=author
        lines.append(parts[0] + "|" + parts[1] + "|" + parts[2] + "\n")
            
    f.close()
    if found==0:
        messagebox.showerror("missing","missing")
    if found==1:
        f=open(FILENAME,"w")
        f.writelines(lines)
        f.close()
        messagebox.showinfo("written","modified")


root=tk.Tk()
root.title("book GUI")
root.geometry("500x500")

tk.Label(root, text = "enter ISBN | bookname | author").pack()

entry_isbn = tk.Entry(root)
entry_isbn.pack()
entry_book = tk.Entry(root)
entry_book.pack()
entry_author = tk.Entry(root)
entry_author.pack()

tk.Button(root, text = "enter", command = add).pack()

tk.Label(root, text = "Search").pack()

entry_search= tk.Entry(root)
entry_search.pack()

tk.Button(root, text = "search", command = search).pack()

tk.Label(root, text = "Modify").pack()

entry_isbn2 = tk.Entry(root)
entry_isbn2.pack()
entry_book2 = tk.Entry(root)
entry_book2.pack()
entry_author2 = tk.Entry(root)
entry_author2.pack()

tk.Button(root, text = "modify", command = modify).pack()


root.mainloop()