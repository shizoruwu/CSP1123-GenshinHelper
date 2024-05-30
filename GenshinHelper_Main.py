# Top - Side / Bar

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ctypes import windll
from PIL import Image, ImageTk

import todo


root = ttk.Window(themename="light_4")
root.title("Genshin Helper")
root.geometry("900x600+100+100")

s = ttk.Style()
s.configure('green.TButton', foreground = "green")
s.configure('bd.TButton', borderwidth=5)
s.configure('font.TLabel', font=("Georgia", 15))
s.configure('fontt.TLabel', font=("Georgia", 15))
s.configure('grey.TFrame', background="grey")

topFrame = ttk.LabelFrame(root)
topFrame.grid(column=1, row=1, sticky=W, padx=5, columnspan=2)
# topFrame.pack(fill=X)
# ttk.Separator(root).grid(column=1, row=2, columnspan=6, pady=5, sticky=EW, ipadx=350)
# ttk.Separator(root).place(x=10, y=60, relwidth=1)
sideBarFrame = ttk.Frame(root)
sideBarFrame.grid(column=1, row=2, sticky=NW, pady=5, ipady=500, ipadx=5)
# sideBarFrame.columnconfigure(1, weight=1)
# content = ttk.LabelFrame(root, text="testing")
# content.grid(column=2, row=3)
root.update()
sideBarFrame.update()
print(sideBarFrame.winfo_width())
title = ttk.Label(topFrame, text=" Genshin Helper", style="font.TLabel", bootstyle="primary")


# setting = ttk.Button(topFrame, text="Setting")
# setting.grid(column=1, row=0, sticky=E, padx=(0, (root.winfo_width() - 350)), pady=(0, 10))

label1 = ttk.Label(root, text="Feat 1 Test")
label1.grid(column=2, row=3)

labe12 = ttk.Label(root, text="Feat 2 Test")
labe12.grid(column=2, row=3)
labe12.grid_remove()

todoFrame = todo.ToDoAppFrame(root)
todoFrame.grid(column=2, row=2, sticky=NW, padx=10, pady=15)
todoFrame.grid_remove()

def feat1():
    labe12.grid_remove()
    todoFrame.grid_remove()
    label1.grid()
    rt.config(bootstyle='primary-outline')
    chr.config(bootstyle='danger')
    td.config(bootstyle='primary-outline')

def feat2():
    label1.grid_remove()
    todoFrame.grid_remove()
    labe12.grid()
    rt.config(bootstyle='danger')
    chr.config(bootstyle='primary-outline')
    td.config(bootstyle='primary-outline')

def todoApp():
    label1.grid_remove()
    labe12.grid_remove()
    todoFrame.grid()
    td.config(bootstyle='danger')
    chr.config(bootstyle='primary-outline')
    rt.config(bootstyle='primary-outline')


unknown = Image.open("C:\\Users\\Jiahe31\\Downloads\\q2 (1).png")
unknownImg = ImageTk.PhotoImage(unknown)
checklist = Image.open("C:\\Users\\Jiahe31\\Downloads\\t1.png")
checklistImg = ImageTk.PhotoImage(checklist)

chr = ttk.Button(sideBarFrame, text="Chacracter", image=unknownImg, compound=LEFT, width=10, padding=10, command=feat1, bootstyle='danger', takefocus=False)
chr.grid(column=0, row=1, padx=10, pady=15)
rt = ttk.Button(sideBarFrame, text="Resin Timer", image=unknownImg, compound=LEFT, width=10, padding=10, command=feat2, bootstyle='primary-outline', takefocus=False)
rt.grid(column=0, row=2, padx=10, pady=(0, 15))
td = ttk.Button(sideBarFrame, text="To-Do List", image=checklistImg, compound=LEFT, width=10, padding=10, command=todoApp, bootstyle='primary-outline', takefocus=False)
td.grid(column=0, row=3, padx=10, pady=(0, 15), sticky=EW)
# ttk.Button(sideBarFrame, width=15, padding=13, bootstyle='primary', takefocus=False).grid(column=0, row=4, sticky=W, ipady=200)

sideBarFrame.update()
title.grid(column=1, row=1, sticky=W, pady=(0, 10), padx=(5, root.winfo_width() - (sideBarFrame.winfo_width() + 50) ))



root.mainloop()