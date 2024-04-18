# To-Do List in-progress

from tkinter import *
from tkinter import ttk

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

# Create some checkbox
b1 = BooleanVar()
b2 = BooleanVar()
b3 = BooleanVar()
checkbox1 = ttk.Checkbutton(frame, variable=b1, text='Checkbox 1')
checkbox2 = ttk.Checkbutton(frame, variable=b2, text='Checkbox 2')
checkbox3 = ttk.Checkbutton(frame, variable=b3, text='Checkbox 3')
# Render
checkbox1.grid(column=1, row=1, pady=5)
checkbox2.grid(column=1, row=2, pady=5)
checkbox3.grid(column=1, row=3, pady=5)

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

print(addB.configure())

root.mainloop()