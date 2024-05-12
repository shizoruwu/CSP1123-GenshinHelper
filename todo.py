# To-Do List in-progress

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from ctypes import windll

class ToDoAppFrame(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)

        self.title_frame = ttk.Frame(self)
        self.title_frame.grid(column=0, row=0, sticky=W)

        # Create Label
        label = ttk.Label(self.title_frame, text="To-Do List", font=("Georgia", 15))
        label.grid(column=1, row=0, padx=(30, 15), pady=20, sticky=W) # Render
        # Create "add" task button
        add = ttk.Button(self.title_frame, text="Add", width=5, command=self.add_task_window)
        add.grid(column=2, row=0, pady=5, sticky=W)
        delete_button = ttk.Button(self.title_frame, text="Delete", width=7, command=self.delete)
        delete_button.grid(column=3, row=0, sticky=W, padx=(5,0))

        s = ttk.Style()
        s.configure('a.TFrame', background='red')
        # , style='a.TFrame'

        # Create a frame for canvas
        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.grid(column=0, row=1, sticky=NW)
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)
        # Make canvas frame able to resizing later
        self.canvas_frame.grid_propagate(False)

        # Create a canvas
        self.canvas = Canvas(self.canvas_frame, highlightthickness=0)
        self.canvas.grid(column=0, row=0, sticky=NSEW)

        # Create a scrollbar and link to canvas
        self.scrollbar = ttk.Scrollbar(self.canvas_frame, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.grid(column=1, row=0, sticky=NS)
        self.canvas.configure(yscrollcommand=self.scrollbar.set) # Link canvas

        self.tasks_frame = ttk.Frame(self.canvas)
        # self.tasks_frame.grid(column=0, row=1, sticky=W)
        
        self.canvas.create_window((0, 0), window=self.tasks_frame, anchor='nw')

        # Update widgets to get w, h to resize canvas frame
        root.update()
        self.title_frame.update()
        # print(root.winfo_width(), root.winfo_height(), root.winfo_rooty(), root.winfo_y())
        # print(self.self.title_frame.winfo_width(), self.self.title_frame.winfo_height())
        title_bar_height = root.winfo_rooty() - root.winfo_y()
        self.canvas_frame.config(width=root.winfo_width(), height=root.winfo_height()
                             - self.title_frame.winfo_height())

        # Connect db
        self.DBconnection = sqlite3.connect("genshindata.db")
        self.DBcursor = self.DBconnection.cursor()

        # Create a table if not exists
        self.DBcursor.execute("CREATE TABLE IF NOT EXISTS tasks(Task, Status)")

        # Init a dict for tasks and its status later
        self.tasks = {}
        # Get raw widget variable name(create_checkbox widget(checkbutton name)) for refresh function
        self.raw_tasks = [] 

        # Read and get values from db
        values = self.DBcursor.execute("SELECT * FROM tasks") # Read
        values = values.fetchall() # Get

        # Add task and status to dict
        for data in values:
            # print(data[1])
            self.tasks[data[0]] = eval(data[1]) # Add items to dict
        print(f"\ndict -> {self.tasks}")
        
        self.create_checkbox(self.tasks_frame)

        # After created checkbox, make scrollbar works
        # update the frame
        self.tasks_frame.update_idletasks()
        # Set canvas scroll region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Resize scrollbar when root size changed
        root.bind('<Configure>', self.resize_canvas_frame)
        root.bind("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

    def add_task_window(self):

        ## Add task function
        def add_task():
            # print(self.text)
            text = self.entry.get()
            if text == '':
                print("Error - Blank")
            elif text not in self.tasks:
                self.DBcursor.execute(f"INSERT INTO tasks VALUES('{text}', 'False')")
                self.tasks[text] = False
                print("Task added.")
            elif text in self.tasks:
                self.DBcursor.execute(f"INSERT INTO tasks VALUES('{text} (1)', 'False')")
                self.tasks[f'{text} (1)'] = False
                print("Task added.")
            self.DBconnection.commit() # Save added task to db
            print(f"\n(add_task) -> {self.tasks}")

            self.add_window.destroy()
            self.refresh()

        # Create a window for add task/s
        self.add_window = Toplevel()
        self.add_window.title("Add Task")
        self.add_window.geometry("+550+150")

        # Create label
        label2 = ttk.Label(self.add_window, text="Add a task...")
        label2.grid(column=0, row=0, pady=(50, 5))
        # Create entry
        self.entry = ttk.Entry(self.add_window)
        self.entry.grid(column=0, row=1, padx=50)
        # Create "add" task button
        add2 = ttk.Button(self.add_window, text="Add", width=5, command=add_task)
        add2.grid(column=0, row=2, pady=(10, 50))

    def delete(self):
         # Create another window
        self.delete_window = Toplevel()
        self.delete_window.title("Delete task")
        self.delete_window.geometry("+550+150")
        
        label2 = ttk.Label(self.delete_window, text="Delete Task/s")
        label2.grid(column=1, row=0)
        # Create listbox
        self.listbox = Listbox(self.delete_window, selectmode=EXTENDED)
        self.listbox.grid(column=1, row=1, padx=10)
        # Insert values to the listbox
        for task in self.tasks:
            self.listbox.insert(END, task)

        button = ttk.Button(self.delete_window, text="Delete", width=8, command=self.delete_func)
        button.grid(column=1, row=2, pady=(10, 10))

    def delete_func(self):
        confirm = messagebox.askyesno(title="Delete Task", message="Are you sure you want to "
                                "delete this/these task?", icon="warning")
        if confirm:
            for selected_listbox_index in self.listbox.curselection():
                # print(listbox.get(selected_listbox_index))
                self.DBcursor.execute(f"DELETE FROM tasks WHERE Task = '{self.listbox.get(selected_listbox_index)}'")
                self.tasks.pop(f"{self.listbox.get(selected_listbox_index)}")
        else:
            self.delete_window.destroy()
        self.DBconnection.commit()
        self.delete_window.destroy()
        self.refresh()

    # Create multiple checkbox
    def create_checkbox(self, master):
        row_init = 1
        for task, status in self.tasks.items():
            var = BooleanVar()
            # if status is BooleanVar, get bool by get func
            if isinstance(status, BooleanVar):
                var2 = status.get()
                var.set(var2)
            elif isinstance(status, bool):
                var.set(status)
            # print(type(status))
            checkbox = ttk.Checkbutton(master, text=task, variable=var, command=self.get_cb_state)
            checkbox.grid(column=1, row=row_init, padx=(30, 0), pady=5, sticky=W)
            self.tasks[task] = var
            self.raw_tasks.append(checkbox)
            row_init += 1
        
        print(f"\ndict(create_checkbox) -> {self.tasks}")

    def refresh(self):
        for var in self.raw_tasks:
            var.destroy()
        self.create_checkbox(self.tasks_frame)

    def get_cb_state(self):
        for task in self.tasks:
            val = self.tasks[task].get() # Get the value(state)
            # Update lastest checkbox value(state) to db
            self.DBcursor.execute(f"UPDATE tasks SET Status = '{val}' WHERE Task = '{task}'")
        self.DBconnection.commit()
        print("Automatically saved checkbox value.")

    def resize_canvas_frame(self, event):
        # Update widgets to get w, h to resize canvas frame

        # print(root.winfo_width(), root.winfo_height(), root.winfo_rooty(), root.winfo_y())
        # print(self.self.title_frame.winfo_width(), self.self.title_frame.winfo_height())
        title_bar_height = root.winfo_rooty() - root.winfo_y()
        self.canvas_frame.config(width=root.winfo_width(), height=root.winfo_height()
                             - self.title_frame.winfo_height())










windll.shcore.SetProcessDpiAwareness(1)

# Create a window
root = Tk()
root.title("To-Do List")
root.geometry("900x600+100+100") # (w, h, x, y)

frame = ToDoAppFrame(root)
frame.grid()

root.mainloop()