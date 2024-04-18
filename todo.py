# To-Do List in-progress

import tkinter as ttk
from tkinter import *

# Create a window
root = Tk()
root.title("To-Do List")
root.geometry("800x400")

# Create a frame inside the window
frame = ttk.Frame(root, borderwidth=10)
frame.grid() # Render

# Create Label
label = ttk.Label(frame, text="To-Do List", font=("TkDefaultFont", 12))
label.grid(column=1, row=0, columnspan=5) # Render

# Create some checkbox
checkbox1 = ttk.Checkbutton(frame, text='Checkbox 1')
checkbox2 = ttk.Checkbutton(frame, text='Checkbox 2')
checkbox3 = ttk.Checkbutton(frame, text='Checkbox 3')
# Render
checkbox1.grid(column=1, row=1, pady=5)
checkbox2.grid(column=1, row=2, pady=5)
checkbox3.grid(column=1, row=3, pady=5)

# Create some button
button1 = ttk.Button(frame, text=" D ")
button2 = ttk.Button(frame, text=" D ")
button3 = ttk.Button(frame, text=" D ")
# Render
button1.grid(column=2, row=1)
button2.grid(column=2, row=2)
button3.grid(column=2, row=3)


root.mainloop()