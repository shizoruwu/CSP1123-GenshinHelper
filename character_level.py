import sqlite3
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

#def
def fetchname():   #fetch name from data base
  conn = sqlite3.connect('genshindata.db')
  cur = conn.cursor()
  cur.execute("SELECT Name FROM CharacterLevel")
  namerows = cur.fetchall()

  global namelist
  namelist = [row[0] for row in namerows]
  namelist.sort()

  conn.close()

fetchname()

#Search Function to Remove Unrelated Object
def Search():
  searchvalue = CharaChosen.get().lower()
  if searchvalue == '':
    CharaChosen['values'] = namelist

  else:
    data = [item for item in namelist if searchvalue in item.lower()]
    CharaChosen['values'] = data

def NewWindow():
  conn = sqlite3.connect('genshindata.db')
  cur = conn.cursor()
  currentname = CharaChosen.get()

  if currentname in namelist:
    cur.execute("SELECT normal_boss FROM CharacterLevel WHERE Name = ?", (currentname,))
    row = cur.fetchone()
    #normal_boss
    if row:
      normal_boss.set(row[0]) 

    NewWindow = tk.Toplevel(root)
    NewWindow.geometry("1000x750")
    NewWindow.title("Character Information")

    #grid
    NewWindow.columnconfigure(0, weight = 1)
    NewWindow.rowconfigure((0,1), weight = 1)
    NewWindow.rowconfigure(2, weight = 10)

    # Add widgets to the new window/frame
    character_info_label = tk.Label(NewWindow, text="Character Information", font=('Arial', 20))
    character_info_label.grid(row = 0, column = 0, columnspan = 2, pady=10)

    #add frame
    frame = ttk.LabelFrame(NewWindow, height = 600, width = 900)
    frame.grid(row = 2, column = 0)

    frame.columnconfigure((0,1,2), weight = 1)
    frame.rowconfigure((0,1,2,3), weight = 1)

    global character_image, normal_boss_image
    character_image = ttk.Label(frame)
    character_image.grid(row = 1, column = 0, rowspan = 4, sticky = 'w')

    normal_boss_image = ttk.Label(frame)
    normal_boss_image.grid(row = 0, column = 1, rowspan = 2, sticky = 'n')

    gemstone_image = ttk.Label(frame)
    gemstone_image.grid(row = 0,column = 2, rowspan = 2, sticky = 'n')

    #pull image inside
    image_path_1 = f"Genshin_Image/{currentname}_Card.png"
    image_1 = Image.open(image_path_1)
    resized_image_1 = image_1.resize((265, 515))
    charphoto = ImageTk.PhotoImage(resized_image_1)
    character_image.config(image=charphoto)
    character_image.image = charphoto
    
    character_name = tk.Label(frame, text=currentname, font=('Arial', 20))
    character_name.grid(row = 0, column = 0) 
    
    image_path_2 = f"Materials/normal boss/{normal_boss.get()}.png"
    image_2 = Image.open(image_path_2)
    resized_image_2 = image_2.resize((100,100))
    norphoto = ImageTk.PhotoImage(resized_image_2)
    normal_boss_image.config(image=norphoto)
    normal_boss_image.image = norphoto
    
    normal_material = tk.Label(frame, text = normal_boss.get(), font=('Arial', 10), width=28)
    normal_material.grid(row = 0, column = 1, rowspan = 2)

    image_path_3 = f"Materials/ascension/{ascension.get()} Gemstone.png"
    image_3 = Image.open(image_path_3)
    resized_image_3 = image_3.resize((100,100))
    gemphoto = ImageTk.PhotoImage(resized_image_3)
    gemstone_image.config(image=gemphoto)
    gemstone_image.image = gemphoto

    gemstone_name = tk.Label(frame, text = f'{ascension.get()} Gemstone', font=('Arial', 10), width=28)
    gemstone_name.grid(row = 0, column = 2, rowspan = 2)
    print(ascension.get())

  else:
    print(f'invalid')

def characterdata():
  conn = sqlite3.connect('genshindata.db')
  cur = conn.cursor()
  currentname = CharaChosen.get()

  if currentname in namelist:
    cur.execute("SELECT normal_boss FROM CharacterLevel WHERE Name = ?", (currentname,))
    row = cur.fetchone()
    if row:
      normal_boss.set(row[0])

    cur.execute("SELECT ascension FROM CharacterLevel WHERE Name = ?", (currentname,))
    row = cur.fetchone()
    if row:
      ascension.set(row[0])

  else:
    print(f"No data found for {currentname}.")

#character calculator features
root = tk.Tk()
root.geometry("1295x785")
root.title("Character Level Calculator")

#grid
root.columnconfigure((0,1,2), weight = 1)
root.rowconfigure((0,1), weight = 1)
root.rowconfigure(2, weight = 10)

#labels
title = tk.Label(root, text = "Select Character to show their Information.", font = ('Arial', 22))
title.grid(row = 0, column = 0, columnspan = 2, sticky = 'w', padx = 20, pady = 10)

search = tk.Label(root, text = "Select Character ", font = ('Arial', 20))
search.grid(row = 1, column = 0, sticky = 'e', pady = (0,6))

#search box
global CharaChosen
boxvalue = tk.StringVar()
CharaChosen = ttk.Combobox(root, textvariable=boxvalue, values=namelist, width=42)
CharaChosen.grid(row = 1, column = 1 , sticky = 'w', padx = (0,20))

global normal_boss, ascension
normal_boss = tk.StringVar()
normal_boss.set('')
ascension = tk.StringVar()
ascension.set('')

AddCharacterButton = ttk.Button(root, text="SEARCH", width = 8,command = NewWindow)
AddCharacterButton.grid(row = 1, column = 1, sticky = 'e', padx = (0,175))

CharaChosen.current()
CharaChosen.bind('<KeyRelease>', Search)

root.mainloop()