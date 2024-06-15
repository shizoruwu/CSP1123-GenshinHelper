# To-Do List in-progress

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from ctypes import windll

class ToDoAppFrame(ttk.LabelFrame):

    def __init__(self, master, *args, **kargs):
        super().__init__(master, *args, **kargs)

        self.master = master
        self.label = ttk.Label(text="To-Do List", style="fontt.TLabel")
        self.config(labelwidget=self.label)


        self.title_frame = ttk.Frame(self)
        self.title_frame.grid(column=0, row=0, sticky=W)

        add = ttk.Button(self.title_frame, text="Add", width=5, command=self.add_task_window)
        add.grid(column=2, row=0, padx=(30, 0), pady=10, sticky=W)
        delete_button = ttk.Button(self.title_frame, text="Delete", width=7, command=self.delete)
        delete_button.grid(column=3, row=0, sticky=W, padx=(5,0))
        self.showHide = ttk.Button(self.title_frame, text="Show Completed Tasks", width=21, command=self.show)
        self.showHide.grid(column=4, row=0, sticky=W, padx=(5,0))
        self.delAllTasks = ttk.Button(self.title_frame, text="Delete All Completed Tasks", width=25, command=self.delAllTaskFunc)
        self.delAllTasks.grid(column=5, row=0, sticky=W, padx=(5,0))
        self.delAllTasks.grid_remove()

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
        self.master.update()
        self.title_frame.update()
        title_bar_height = self.master.winfo_rooty() - self.master.winfo_y()
        self.canvas_frame.config(width=self.master.winfo_width() - 230, height=self.master.winfo_height()
                             - self.title_frame.winfo_height() - 200)

        # Init a dict for tasks and its status later
        self.dictionary = {}
        # Get raw widget variable name(create_checkbox widget(checkbutton name)) for refresh function
        self.raw_tasks = [] 

        # Add task and status to dict
        for data in self.database("fetch"):
            self.dictionary[data[0]] = eval(data[1]) # Add items to dict
        self.tasks = dict(sorted(self.dictionary.items(), key=lambda item: item[1]))

        
        self.create_checkbox(self.tasks_frame)

        # After created checkbox, make scrollbar works
        # update the frame
        self.tasks_frame.update_idletasks()
        # Set canvas scroll region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Resize scrollbar when root size changed
        # self.master.bind('<Configure>', self.resize_canvas_frame)
        self.master.bind("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

    def database(self, action, query=None):
        # Connect db
        self.DBconnection = sqlite3.connect("genshindata.db")
        self.DBcursor = self.DBconnection.cursor()
        # Create a table if not exists
        self.DBcursor.execute("CREATE TABLE IF NOT EXISTS tasks(Task, Status)")

        if action == "fetch":
            # Read and get values from db
            data = self.DBcursor.execute("SELECT * FROM tasks") # Read
            self.data = data.fetchall() # Get
            return self.data

        elif action == "others":
            self.DBcursor.execute(query)
        
        self.DBconnection.commit()
        self.DBconnection.close()

    # Create multiple checkbox
    def create_checkbox(self, master, showCompletedTasks=False):
        row_init = 1
        self.sortedTasks = dict(sorted(self.tasks.items(), key=lambda item: item[1]))
        for task, status in self.sortedTasks.items():

            var = BooleanVar()
            var.set(status)
            if showCompletedTasks == False:
                if self.sortedTasks[task] == False:
                    checkbox = ttk.Checkbutton(master, text=task, variable=var, command=lambda show=showCompletedTasks: self.get_cb_state(show))
                    checkbox.grid(column=1, row=row_init, padx=(30, 0), pady=5, sticky=W)
                else:
                    print("No Tasks.")
            else:
                checkbox = ttk.Checkbutton(master, text=task, variable=var, command=lambda show=showCompletedTasks: self.get_cb_state(show))
                checkbox.grid(column=1, row=row_init, padx=(30, 0), pady=5, sticky=W)
            # Keep a refrence for checkbox value
            self.sortedTasks[task] = var
            # Add checkbox variable to a list for refresh function
            self.raw_tasks.append(checkbox)
            row_init += 1

    def show(self):
        self.delAllTasks.grid()
        self.showHide.config(text="Hide Completed Tasks", command=self.hide)
        self.refresh(True)

    def hide(self):
        self.delAllTasks.grid_remove()
        self.showHide.config(text="Show Completed Tasks", command=self.show)
        self.refresh()
        
    def add_task_window(self):

        ## Add task function
        def add_task(a):
            text = self.entry.get()
            if text == '':
                print("Error - Blank")
            elif text not in self.tasks:
                self.database("others", f"""INSERT INTO tasks VALUES("{text}", "False")""")
                self.tasks[text] = False
                print("Task added.")
            elif text in self.tasks:
                self.database("others", f"""INSERT INTO tasks VALUES("{text} (copy)", "False")""")
                self.tasks[f'{text} (1)'] = False
                print("Task added.")

            self.add_window.destroy()
            self.refresh()

        # Create a window for add task/s
        self.add_window = Toplevel()
        self.add_window.title("Add Task")
        self.add_window.geometry("+550+150")

        # Add window widgets
        label2 = ttk.Label(self.add_window, text="Add a task...")
        label2.grid(column=0, row=0, pady=(50, 5))
        self.entry = ttk.Entry(self.add_window)
        self.entry.grid(column=0, row=1, padx=50)
        add2 = ttk.Button(self.add_window, text="Add", width=5, command=add_task)
        add2.grid(column=0, row=2, pady=(10, 50))
        add2.bind('<Return>', add_task)
        self.entry.bind('<Return>', add_task)

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
                self.database("others", f"""DELETE FROM tasks WHERE Task = "{self.listbox.get(selected_listbox_index)}" """)
                self.tasks.pop(f"{self.listbox.get(selected_listbox_index)}")
                
        else:
            self.delete_window.destroy()

        self.delete_window.destroy()
        self.refresh()


    def refresh(self, showCompletedTasks=False):
        for var in self.raw_tasks:
            var.destroy()
        self.tasks.clear()
        self.dictionary.clear()
        self.raw_tasks.clear()
        self.sortedTasks.clear()
        for data in self.database("fetch"):
            self.dictionary[data[0]] = eval(data[1]) # Add items to dict
        self.tasks = dict(sorted(self.dictionary.items(), key=lambda item: item[1]))
        self.create_checkbox(self.tasks_frame, showCompletedTasks)

    def get_cb_state(self, showCompletedTasks):
        for task in self.sortedTasks:
            self.tasks[task] = self.sortedTasks[task].get() # Get the value(state)
            # Update lastest checkbox value(state) to db
            self.database("others", f"""UPDATE tasks SET Status = "{self.sortedTasks[task].get()}" WHERE Task = "{task}" """)

        notice = ttk.Label(self.title_frame, text="Task Checked/Unchecked")
        notice.grid(column=6, row=0, sticky=W, padx=5)

        if showCompletedTasks:
            self.refresh(True)
        else:
            self.refresh()

    def delAllTaskFunc(self):
        
        temp = self.tasks.copy()
        self.tasks.clear()
        for task, status in temp.items():
            if status == False:
                self.tasks[task] = status
            elif status:
                self.database("others", f"""DELETE FROM tasks WHERE Task = "{task}" """)
        
        self.hide()
        self.refresh(False)

    def resize_canvas_frame(self, event):
        # Update widgets to get w, h to resize canvas frame

        # print(root.winfo_width(), root.winfo_height(), root.winfo_rooty(), root.winfo_y())
        # print(self.self.title_frame.winfo_width(), self.self.title_frame.winfo_height())
        title_bar_height = self.master.winfo_rooty() - self.master.winfo_y()
        self.canvas_frame.config(width=self.master.winfo_width() - 180, height=self.master.winfo_height()
                             - self.title_frame.winfo_height() - 200)


def main():
    windll.shcore.SetProcessDpiAwareness(1)

    # Create a window
    root = Tk()
    root.title("To-Do List")
    root.geometry("900x600+100+100") # (w, h, x, y)

    frame = ToDoAppFrame(root)
    frame.grid()

    root.mainloop()

if __name__ == "__main__":
    main()