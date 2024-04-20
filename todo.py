# To-Do List in-progress

from tkinter import *
from tkinter import ttk
import sqlite3

# Create a window
root = Tk()
root.title("To-Do List")
root.geometry("800x400")

# Create a frame inside the window
frame = ttk.Frame(root, borderwidth=10)
frame.grid(column=0, row=0) # Render

# Create Label
label = ttk.Label(frame, text="To-Do List", font=("TkDefaultFont", 12))
label.grid(column=1, row=0, columnspan=5) # Render

# Connect db
DBconnection = sqlite3.connect("tasks.db")
DBcursor = DBconnection.cursor()

# Create a table if not exists
DBcursor.execute("CREATE TABLE IF NOT EXISTS tasks(Task, Status)")

# Init a dict for tasks and its status later
tasks = {}

# Read and get values from db
values = DBcursor.execute("SELECT * FROM tasks") # Read
values = values.fetchall() # Get

# Add task and status to dict
def db2dict():
    for data in values:
        # print(data[1])
        tasks[data[0]] = eval(data[1]) # Add items to dict
    print(f"Dict: {tasks}")

db2dict()

# Create "add" task button
addB = ttk.Button(frame, text="add", width=5)
addB.grid(column=1, row=4, pady=5, sticky=W)

# Create some button
button1 = ttk.Button(frame, text="Delete", width=6)
button2 = ttk.Button(frame, text="Delete", width=6)
button3 = ttk.Button(frame, text="Delete", width=6)
# Render
button1.grid(column=2, row=1, padx=10)
button2.grid(column=2, row=2)
button3.grid(column=2, row=3)

# print(addB.configure())

root.mainloop()