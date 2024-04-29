###Testing for search function

import sqlite3 
import tkinter as tk
from tkinter import ttk 
from PIL import ImageTk, Image

FiveStarCharacter = ['Albedo','Alhaitam','Arlecchino','Aloy','Arataki Itto','Baizhu','Chiori','Cyno','Dehya','Diluc','Eula','Furina','Ganyu','Hu Tao','Jean','Kaedehara Kazuha','Kamisato Ayaka','Kamisato Ayato','Keqing','Klee','Lyney','Mona','Nahida','Navia','Neuvillette','Nilou','Qiqi','Raiden Shogun','Sangonomiya Kokomi','Shenhe','Tartagila','Tighnari','Traveler','Venti','Wanderer','Wriothesley','Xianyun','Xiao','Yae Miko','Yelan','Yoimiya','Zhongli']

class charactersearch(tk.Tk):
    def __init__(self):
      tk.Tk.__init__(self)

      self.title('Character Search')
      self.geometry('800x450')

      ttk.Label(self, text = "Select Character to show their Informations.", 
      font = ("Times New Roman", 15)).grid(columnspan = 2, row = 1, padx = 10, pady = 15) 

      ttk.Label(self, text = "Select Character :", 
      font = ("Times New Roman", 18)).grid(column = 0, row = 2, pady = 20,sticky = 'e') 

      #Search Box Combobox  
      global CharaChosen
      global boxvalue
      boxvalue = tk.StringVar
      fetchname()
      CharaChosen = ttk.Combobox(self,font = ("Times New Roman", 12),values=namelist,width=20,textvariable=boxvalue)
      CharaChosen.grid(column = 1, row = 2 , padx = 20, pady = 20 )
      CharaChosen.current()
      CharaChosen.bind('<KeyRelease>',search)

      #Buttons to Enter Character Names
      EnterButton = ttk.Button(self, text="SEARCH", width = 8,command = CharacterDataFetch)
      EnterButton.grid(column = 2, row = 2, padx = 18, pady = 20 )

      #Pulled Data from Search
      global CharacterName
      global CharacterElement
      global CharacterWeapon
      global CharacterRegion
      global CharacterPhoto

      CharacterName = tk.StringVar()
      CharacterElement = tk.StringVar()
      CharacterWeapon = tk.StringVar()
      CharacterRegion = tk.StringVar()
      CharacterPhoto = ImageTk.PhotoImage(Image.new('RGBA', (200, 300), (0, 0, 0, 0)))

      CharacterName.set(' ')
      CharacterElement.set(' ')
      CharacterWeapon.set(' ')
      CharacterRegion.set(' ')

      ttk.Label(self,text = "Character Name :", font = ("Times New Roman",18)).grid(column = 0,row = 4,pady = 5,sticky = 'e')
      ttk.Label(self,textvariable = CharacterName, font = ("Times New Roman",18)).grid(column = 1,row = 4,padx = 15,pady = 5,sticky = 'w')

      ttk.Label(self,text = "Character Element :", font = ("Times New Roman",18)).grid(column = 0,row = 5,pady = 5,sticky = 'e')
      ttk.Label(self,textvariable = CharacterElement, font = ("Times New Roman",18)).grid(column = 1,row = 5,padx = 15,pady = 5,sticky = 'w')

      ttk.Label(self,text = "Character Weapon :", font = ("Times New Roman",18)).grid(column = 0,row = 6,pady = 5,sticky = 'e')
      ttk.Label(self,textvariable = CharacterWeapon, font = ("Times New Roman",18)).grid(column = 1,row = 6,padx = 15,pady = 5,sticky = 'w')

      ttk.Label(self,text = "Character Region :", font = ("Times New Roman",18)).grid(column = 0,row = 7,pady = 5,sticky = 'e')
      ttk.Label(self,textvariable = CharacterRegion, font = ("Times New Roman",18)).grid(column = 1,row = 7,padx = 15,pady = 5,sticky = 'w')

      ttk.Label(self,image = CharacterPhoto).grid(column = 3,row = 2,rowspan = 6,sticky = 'e')
      
#Pull Data From SQLite for dropdown listbox names
def fetchname():
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
def CharacterDataFetch():
  conn = sqlite3.connect('genshindata.db')
  cursor = conn.cursor()
  currentname = CharaChosen.get()
  
  if currentname in namelist:
    #Fetch Character Name
    cursor.execute("SELECT Name FROM Characterdata WHERE Name = ?", (currentname,))
    row = cursor.fetchone()
    if row:
      CharacterName.set(row[0])

    #Fetch Character Element
    cursor.execute("SELECT Element FROM Characterdata WHERE Name = ?", (currentname,))
    row = cursor.fetchone()
    if row:
      CharacterElement.set(row[0])

    cursor.execute("SELECT WeaponType FROM Characterdata WHERE Name = ?", (currentname,))
    row = cursor.fetchone()
    if row:
      CharacterWeapon.set(row[0])

    cursor.execute("SELECT Region FROM Characterdata WHERE Name = ?", (currentname,))
    row = cursor.fetchone()
    if row:
      CharacterRegion.set(row[0])

    #Show Character Image
    file_name = currentname

    image_path = f"Genshin_Image/{file_name}_Card.webp"
    image = Image.open(image_path)
    resized_image = image.resize((200, 600))
    charphoto = ImageTk.PhotoImage(resized_image)
    charimg



  #Remove data if Name = False
  else:
    CharacterName.set('Please Enter A Valid Name')
    CharacterElement.set(' ')
    CharacterWeapon.set(' ')
    CharacterRegion.set(' ')
    
  conn.close()

  return CharacterName

#Search Function to Remove Unrelated Object
def search(self):
  searchvalue = self.widget.get()
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