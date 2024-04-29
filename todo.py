# To-Do List in-progress

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
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
# Get raw widget variable name(create_checkbox widget(checkbutton name)) for refresh function
raw_tasks = [] 

# Read and get values from db
values = DBcursor.execute("SELECT * FROM tasks") # Read
values = values.fetchall() # Get

# Add task and status to dict
for data in values:
    # print(data[1])
    tasks[data[0]] = eval(data[1]) # Add items to dict
print(f"dict -> {tasks}")

# Create entry
entry = ttk.Entry(frame)
entry.grid(column=2, row=0, padx=(50, 5))

## Add task function
def add_task():
    # print(entry.get())
    text = entry.get()
    if text == '':
        print("Error - Blank")
    elif text not in tasks:
        DBcursor.execute(f"INSERT INTO tasks VALUES('{text}', 'False')")
        tasks[text] = False
        print("Task added.")
    elif text in tasks:
        DBcursor.execute(f"INSERT INTO tasks VALUES('{text} (1)', 'False')")
        tasks[text] = False
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
        # if status is BooleanVar, get bool by get func
        if isinstance(status, BooleanVar):
            var2 = status.get()
            var.set(var2)
        elif isinstance(status, bool):
            var.set(status)
        # print(type(status))
        checkbox = ttk.Checkbutton(frame, text=task, variable=var)
        checkbox.grid(column=1, row=row_init, padx=(20, 0), pady=3, sticky=W)
        tasks[task] = var
        raw_tasks.append(checkbox)
        row_init += 1
    
    print(f"\ndict(create_checkbox) -> {tasks}")

def refresh():
    for var in raw_tasks:
        var.destroy()
    create_checkbox()

refreshb = ttk.Button(frame, text="Refresh", width=9, command=refresh)
refreshb.grid(column=4, row=0, sticky=W, padx=(5, 0))

# print(add.configure())
create_checkbox()


# Delete function
def delete():
    # Create another window
    delete_window = Toplevel()
    delete_window.title("Delete task")
    delete_window.geometry("150x250+550+150")
    
    frame2 = ttk.Frame(delete_window, padding=10)
    frame2.grid(column=0, row=0, padx=5, pady=5)
    label2 = ttk.Label(frame, text="Delete Task")
    # Create listbox
    listbox = Listbox(frame2, selectmode=EXTENDED)
    listbox.grid(column=1, row=1)
    # Insert values to the listbox
    for task in tasks:
        listbox.insert(END, task)

    def delete_func():
        confirm = messagebox.askyesno(title="Delete Task", message="Are you sure you want to "
                                "delete this/these task?", icon="warning")
        if confirm:
            for selected_listbox_index in listbox.curselection():
                # print(listbox.get(selected_listbox_index))
                DBcursor.execute(f"DELETE FROM tasks WHERE Task = '{listbox.get(selected_listbox_index)}'")
                tasks.pop(f"{listbox.get(selected_listbox_index)}")
        else:
            delete_window.destroy()
        DBconnection.commit()
        delete_window.destroy()
        for raw_task in raw_tasks:
            raw_task.destroy()
        create_checkbox(frame)

    button = ttk.Button(frame2, text="Delete", width=8, command=delete_func)
    button.grid(column=1, row=2, pady=(10, 0))

delete_button = ttk.Button(frame, text="Delete", width=8, command=delete)
delete_button.grid(column=5, row=0, sticky=W, padx=(5,0))


root.mainloop()