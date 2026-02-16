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
    result=""
    f=open(FILENAME,"r")
    for line in f
        if key in line
            result = result + line
    if result ==""

    else 

def modify():
    isbn= entry_isbn2.get()
    book= entry_book2.get()
    author= entry_author2.get()
    f= open(FILENAME,"a")
    f = open(FILENAME,"r")
    found=0
    lines=[]

    for line in f
        parts= line.strip().split("|")

            if parts[0]=isbn
                found=1
                part[1]=book
                part[2]=auth
            lines.append(part[0]+ part[1+part[2]])
    f.close()
    if found=1
        f=open(FILENAME,"w")
        f.writelines(lines)
        
        f.close()











root=tk.Tk()
root.title("GUI BOOKS")
root.geometry("400x400")

tk.Label(root, text= "Enter").pack()
entry_isbn=tk.Entry(root)
entry_isbn.pacl()


root.mainloop()