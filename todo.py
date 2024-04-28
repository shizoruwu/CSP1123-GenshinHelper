# To-Do List in-progress

from tkinter import *
from tkinter import ttk
import sqlite3

# Create a window
root = Tk()
root.title("To-Do List")
root.geometry("800x400+100+100") # (w, h, x, y)

# Create a frame inside the window
frame = ttk.Frame(root, borderwidth=10)
frame.grid(column=0, row=0) # Render

# Create Label
label = ttk.Label(frame, text="To-Do List", font=("Georgia", 15))
label.grid(column=1, row=0, padx=(20, 5), pady=10, sticky=W) # Render

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
    print(f"dict(db2dict) -> {tasks}")



# Create entry
entry = ttk.Entry(frame)
entry.grid(column=2, row=0, padx=(50, 5))

def add_task():
    # print(entry.get())
    text = entry.get()
    if text == '':
        print("Error - Blank")
    elif text not in tasks:
        DBcursor.execute(f"INSERT INTO tasks VALUES('{text}', 'False')")
        print("Task added.")
    elif text in tasks:
        DBcursor.execute(f"INSERT INTO tasks VALUES('{text} (1)', 'False')")
        print("Task added.")
    DBconnection.commit() # Save added task to db
    

# Create "add" task button
add = ttk.Button(frame, text="Add", width=5, command=add_task)
add.grid(column=3, row=0, pady=5, sticky=W)

# Create multiple checkbox
def create_checkbox():
    row_init = 1
    for task, status in tasks.items():
        var = BooleanVar()
        var.set(status)
        # print(type(status))
        checkbox = ttk.Checkbutton(frame, text=task, variable=var)
        checkbox.grid(column=1, row=row_init, padx=(20, 0), pady=3, sticky=W)
        tasks[task] = var
        row_init += 1
    
    print(f"\ndict(create_checkbox) -> {tasks}")

# print(add.configure())
db2dict()
create_checkbox()


root.mainloop()