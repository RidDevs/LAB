import tkinter as tk
from tkinter import messagebox

FILENAME="G.txt"

def add():

    isbn= entry_isbn.get()
    book= entry_book.get()
    author= entry_isbn.get()

    f=open(FILENAME,"a")
    f.write()


def search():
    key= entry_isbn.get()
    
def modify():










root=tk.Tk()
root.title("GUI BOOKS")
root.geometry("400x400")

tk.Label(root, text= "Enter").pack()
entry_isbn=tk.Entry(root)
entry_isbn.pacl()


root.mainloop()