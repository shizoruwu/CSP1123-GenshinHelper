# To-Do List in-progress

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

# Create a window
root = Tk()
root.title("To-Do List")
root.geometry("900x600+100+100") # (w, h, x, y)

# Create a frame inside the window
frame = ttk.Frame(root, borderwidth=10)
frame.grid(column=0, row=0) # Render

# Create Label
label = ttk.Label(frame, text="To-Do List", font=("Georgia", 15))
label.grid(column=1, row=0, padx=(30, 15), pady=20, sticky=W) # Render

# Connect db
DBconnection = sqlite3.connect("genshindata.db")
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

def refresh():
    for var in raw_tasks:
        var.destroy()
    create_checkbox()

# Save checkbutton state
def get_cb_state():
    for task in tasks:
        val = tasks[task].get() # Get the value(state)
        # Update lastest checkbox value(state) to db
        DBcursor.execute(f"UPDATE tasks SET Status = '{val}' WHERE Task = '{task}'")
    DBconnection.commit()
    print("Automatically saved checkbox value.")

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
        checkbox = ttk.Checkbutton(frame, text=task, variable=var, command=get_cb_state)
        checkbox.grid(column=1, row=row_init, padx=(30, 0), pady=5, sticky=W)
        tasks[task] = var
        raw_tasks.append(checkbox)
        row_init += 1
    
    print(f"\ndict(create_checkbox) -> {tasks}")

create_checkbox()

## Add task function
def add_task_window():

    def add_task():
        text = entry.get()
        if text == '':
            print("Error - Blank")
        elif text not in tasks:
            DBcursor.execute(f"INSERT INTO tasks VALUES('{text}', 'False')")
            tasks[text] = False
            print("Task added.")
        elif text in tasks:
            DBcursor.execute(f"INSERT INTO tasks VALUES('{text} (1)', 'False')")
            tasks[f'{text} (1)'] = False
            print("Task added.")
        DBconnection.commit() # Save added task to db

        add_window.destroy()
        refresh()

    # Create a window for add task/s
    add_window = Toplevel()
    add_window.title("Add Task")
    add_window.geometry("+550+150")

    # Create label
    label2 = ttk.Label(add_window, text="Add a task...")
    label2.grid(column=0, row=0, pady=(50, 5))
    # Create entry
    entry = ttk.Entry(add_window)
    entry.grid(column=0, row=1, padx=50)
    # Create "add" task button
    add2 = ttk.Button(add_window, text="Add", width=5, command=add_task)
    add2.grid(column=0, row=2, pady=(10, 50))

# Create "add" task button
add = ttk.Button(frame, text="Add", width=5, command=add_task_window)
add.grid(column=3, row=0, pady=5, sticky=W)

# Delete function
def delete():
    # Create another window
    delete_window = Toplevel()
    delete_window.title("Delete task")
    delete_window.geometry("+550+150")
    
    frame3 = ttk.Frame(delete_window, padding=10)
    frame3.grid(column=0, row=0, padx=5, pady=5)
    label2 = ttk.Label(frame3, text="Delete Task/s")
    label2.grid(column=1, row=0)
    # Create listbox
    listbox = Listbox(frame3, selectmode=EXTENDED)
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
        create_checkbox()

    button = ttk.Button(frame3, text="Delete", width=8, command=delete_func)
    button.grid(column=1, row=2, pady=(10, 0))

delete_button = ttk.Button(frame, text="Delete", width=8, command=delete)
delete_button.grid(column=5, row=0, sticky=W, padx=(5,0))




root.mainloop()