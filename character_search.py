###Testing for search function

import sqlite3 
import tkinter as tk
from tkinter import ttk 
from PIL import ImageTk, Image
from ctypes import windll

#FIX BLURRY FONTS
windll.shcore.SetProcessDpiAwareness(1)

class charactersearch(tk.Tk):
  def __init__(self):
    tk.Tk.__init__(self)

    self.title('Character Search')
    self.geometry('1295x785')
    
    TitleChara = ttk.Label(self, text = "Select Character to show their Informations.",
    font = ("Arial", 22)).grid(columnspan = 3, row = 1, padx = 35, pady = 15,sticky = 'w') 

    Searchtext = ttk.Label(self, text = "Select Character ", 
    font = ("Arial", 20)).grid(column = 0, row = 2, padx = 15 , pady = 10,sticky = 'e') 

    #Search Box Combobox
    global CharaChosen
    global boxvalue
    boxvalue = tk.StringVar()
    self.fetchname()
    CharaChosen = ttk.Combobox(self, font = ("Arial", 12),values=namelist,width=32,textvariable=boxvalue)
    CharaChosen.grid(column = 1, row = 2 , padx = 20, pady = 20 , sticky = 'w')
    CharaChosen.current()
    CharaChosen.bind('<KeyRelease>',self.Search)

    #Buttons to Enter Character Names
    EnterButton = ttk.Button(self, text="SEARCH", width = 8,command = self.CharacterDataFetch)
    EnterButton.grid(column = 2, row = 2, padx = 18, pady = 20 , sticky = 'w' )

    #Pulled Data from Search
    global CharacterName , CharacterStar , CharacterElement , CharacterWeapon , CharacterRegion , CharacterPhoto , CharacterBirthday , CharacterInfo

    CharacterName = tk.StringVar()
    CharacterStar = tk.StringVar()
    CharacterElement = tk.StringVar()
    CharacterWeapon = tk.StringVar()
    CharacterRegion = tk.StringVar()
    CharacterBirthday = tk.StringVar()
    CharacterInfo = tk.StringVar()
    CharacterPhoto = ImageTk.PhotoImage(Image.new('RGBA', (200, 300), (0, 0, 0, 0)))

    CharacterName.set(' ')
    CharacterStar.set(' ')
    CharacterElement.set(' ')
    CharacterWeapon.set(' ')
    CharacterRegion.set(' ')
    CharacterBirthday.set(' ')
    CharacterInfo.set(' ')
    
    CharaName = ttk.Label(self,text = "Character Name :" , font = ("Arial",15)).grid(column = 0,row = 4,pady = 5,sticky = 'e')
    CharaNameData = ttk.Label(self,width = 36 , textvariable = CharacterName, font = ("Arial",15)).grid(column = 1,row = 4,padx = 15,pady = 5,sticky = 'w')

    CharStar = ttk.Label(self,text = "Character Star :", font = ("Arial",15)).grid(column = 0,row = 5,pady = 5,sticky = 'e')
    CharaStarData = ttk.Label(self,textvariable = CharacterStar, font = ("Arial",15)).grid(column = 1,row = 5,padx = 15,pady = 5,sticky = 'w')

    CharElement = ttk.Label(self,text = "Character Element :", font = ("Arial",15)).grid(column = 0,row = 6,pady = 5,sticky = 'e')
    CharaElementData = ttk.Label(self,textvariable = CharacterElement, font = ("Arial",15)).grid(column = 1,row = 6,padx = 15,pady = 5,sticky = 'w')

    CharWeapon = ttk.Label(self,text = "Character Weapon :", font = ("Arial",15)).grid(column = 0,row = 7,pady = 5,sticky = 'e')
    CharWeaponData = ttk.Label(self,textvariable = CharacterWeapon, font = ("Arial",15)).grid(column = 1,row = 7,padx = 15,pady = 5,sticky = 'w')

    CharRegion = ttk.Label(self,text = "Character Region :", font = ("Arial",15)).grid(column = 0,row = 8,pady = 5,sticky = 'e')
    CharRegionData = ttk.Label(self,textvariable = CharacterRegion, font = ("Arial",15)).grid(column = 1,row = 8,padx = 15,pady = 5,sticky = 'w')
    
    CharBirthday = ttk.Label(self,text = "Character Birthday :", font = ("Arial",15)).grid(column = 0,row = 9,pady = 5,sticky = 'e')
    CharBirthdayData = ttk.Label(self,textvariable = CharacterBirthday, font = ("Arial",15)).grid(column = 1,row = 9,padx = 15,pady = 5,sticky = 'w')
    
    CharInfo = ttk.Label(self,text = "Character Info :", font = ("Arial",15)).grid(column = 0,row = 10,pady = 5,sticky = 'ne')
    CharInfoData = ttk.Label(self,textvariable = CharacterInfo , wraplength = 600 , font = ("Arial",12)).grid(column = 1,row = 10,padx = 15,pady = 5,sticky = 'w')
    
    CharEmptyRow = ttk.Label(self,text = ' ').grid(columnspan = 3 , row = 11 , pady = 60)

    global CharacterImage
    CharacterImage = ttk.Label(self)
    CharacterImage.grid(column = 2,row = 3,rowspan = 10,sticky = 'ne')
    
  #Pull Data From SQLite for dropdown listbox names
  def fetchname(self):
    conn = sqlite3.connect('genshindata.db')
    cur = conn.cursor()
    cur.execute("SELECT Name FROM Characterdata")
    namerows = cur.fetchall()
      
    #Global Variable Namelist to pull
    global namelist
    namelist = [row[0] for row in namerows]
    namelist.sort()

    conn.close()
    
  #Data Fetch From Selection
  def CharacterDataFetch(self):
    conn = sqlite3.connect('genshindata.db')
    cursor = conn.cursor()
    currentname = CharaChosen.get()
    
    if currentname in namelist:
      #Fetch Character Name
      cursor.execute("SELECT Name FROM Characterdata WHERE Name = ?", (currentname,))
      row = cursor.fetchone()
      if row:
        CharacterName.set(row[0])

      #Determine Character Star
      cursor.execute("SELECT Star FROM Characterdata WHERE Name = ?", (currentname,))
      row = cursor.fetchone()
      if row:
        TemporaryCharStar = int(row[0])
        if TemporaryCharStar == 1:
          CharacterStar.set('5 Star')
        else:
          CharacterStar.set('4 Star')

      #Fetch Character Element
      cursor.execute("SELECT Element FROM Characterdata WHERE Name = ?", (currentname,))
      row = cursor.fetchone()
      if row:
        CharacterElement.set(row[0])

      #Fetch Character Weapon Type
      cursor.execute("SELECT WeaponType FROM Characterdata WHERE Name = ?", (currentname,))
      row = cursor.fetchone()
      if row:
        CharacterWeapon.set(row[0])

      #Fetch Character Region
      cursor.execute("SELECT Region FROM Characterdata WHERE Name = ?", (currentname,))
      row = cursor.fetchone()
      if row:
        CharacterRegion.set(row[0])

      #Fetch Character Birthday
      cursor.execute("SELECT Birthday FROM Characterdata WHERE Name = ?", (currentname,))
      row = cursor.fetchone()
      if row:
        CharacterBirthday.set(row[0])
      
      #Fetch Character Info
      cursor.execute("SELECT Info FROM Characterdata WHERE Name = ?", (currentname,))
      row = cursor.fetchone()
      if row:
        CharacterInfo.set(row[0])

      #Show Character Image
      try:
        # Show Character Image
        image_path = f"Genshin_Image/{currentname}_Card.png"
        image = Image.open(image_path)
        resized_image = image.resize((265, 515))
        charphoto = ImageTk.PhotoImage(resized_image)
        CharacterImage.config(image=charphoto)
        CharacterImage.image = charphoto  # Keep a reference to prevent image from being garbage collected
      except FileNotFoundError:
        print("Image not found:", image_path)
        CharacterImage.config(image=CharacterPhoto)
      
    #Remove data if Name = False
    else:
      CharacterName.set('Please Enter A Valid Name')
      CharacterStar.set (' ')
      CharacterElement.set(' ')
      CharacterWeapon.set(' ')
      CharacterRegion.set(' ')
      CharacterImage.config(image=CharacterPhoto)
    
    boxvalue.set('')
    conn.close()

  #Search Function to Remove Unrelated Object
  def Search(self,event):
    searchvalue = CharaChosen.get()
    if searchvalue == '':
      CharaChosen['values'] = namelist

    else:
      data = []
      for item in namelist:
        if searchvalue.lower() in item.lower():
          data.append(item)
      
      CharaChosen['values'] = data 

#RUN WINDOW
CurrentScreen = charactersearch()
CurrentScreen.mainloop()