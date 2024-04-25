###Testing for search function

import sqlite3 
import tkinter as tk
from tkinter import ttk 
from PIL import ImageTk, Image

FiveStarCharacter = ['Albedo','Alhaitam','Aloy','Arataki Itto'
            ,'Baizhu','Chiori'
            ,'Cyno','Dehya','Diluc','Eula'
            ,'Furina','Ganyu','Hu Tao'
            ,'Jean','Kaedehara Kazuha','Kamisato Ayaka'
            ,'Kamisato Ayato','Keqing','Klee'
            ,'Lyney','Mona','Nahida','Navia','Neuvillette'
            ,'Nilou','Qiqi','Raiden Shogun'
            ,'Sangonomiya Kokomi','Shenhe'
            ,'Tartagila','Tighnari','Traveler','Venti'
            ,'Wanderer','Wriothesley','Xianyun','Xiao'
            ,'Yae Miko','Yelan','Yoimiya','Zhongli']

class charactersearch(tk.Tk):
    def __init__(self):
        
      tk.Tk.__init__(self)

      self.title('Character Search')
      self.wm_minsize(width=800,height=450)

      ttk.Label(self, text = "Select Character to show their Informations.", 
      font = ("Times New Roman", 15)).grid(column = 0, row = 1, padx = 10, pady = 15) 

      ttk.Label(self, text = "Select Character :", 
      font = ("Times New Roman", 12)).grid(column = 0, row = 2, padx = 0, pady = 5) 
        
      global CharaChosen
      global boxvalue
      boxvalue = tk.StringVar
      fetchname()
      CharaChosen = ttk.Combobox(self,font = ("Times New Roman", 12),values=namelist,width=20,textvariable=boxvalue)
      CharaChosen.grid(column = 1, row = 2 , padx = 5, pady = 5 )
      CharaChosen.current()
      CharaChosen.bind('<KeyRelease>',search)

      #Buttons to Enter Character Names
      EnterButton = ttk.Button(self, text="ENTER", width = 8,command = CharacterDataFetch)
      EnterButton.grid(column = 2, row = 2, padx = 18, pady = 5 )

      global CharacterName
      CharacterName = tk.StringVar()
      CharacterName.set(' ')
      ttk.Label(self,text = "CharacterName :", font = ("Times New Roman",18)).grid(column = 0,row = 4,pady = 20)
      ttk.Label(self,textvariable = CharacterName, font = ("Times New Roman",18)).grid(column = 1,row = 4,pady = 20)

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
  
# Work In Progress (Data Fetch From Selection)
def CharacterDataFetch():
  conn = sqlite3.connect('genshindata.db')
  cursor = conn.cursor()
  currentname = CharaChosen.get()
  
  if currentname in namelist:
    cursor.execute("SELECT Name FROM Characterdata WHERE Name = ?", (currentname,))
    row = cursor.fetchone()
    if row:
      CharacterName.set(row[0])
    
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