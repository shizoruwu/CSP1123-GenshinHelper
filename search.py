###Testing for search function

import sqlite3 
import tkinter as tk
from tkinter import ttk 
from PIL import ImageTk, Image

#Character List Names ( DATA )
CharaLst = ['Albedo','Alhaitam','Aloy','Amber','Arataki Itto'
            ,'Baizhu','Barbara','Beidou','Bennett','Candace'
            ,'Charlotte','Chevreuse','Chiori','Chongyun','Collei'
            ,'Cyno','Dehya','Diluc','Diona','Dori','Eula','Faruzan'
            ,'Fischl','Freminet','Furina','Gaming','Ganyu','Hu Tao'
            ,'Jean','Kaedehara Kazuha','Kaeya','Kamisato Ayaka'
            ,'Kamisato Ayato','Kaveh','Keqing','Kirara','Klee'
            ,'Kujou Sara','Kuki Shinobu','Layla','Lisa','Lynette'
            ,'Lyney','Mika','Mona','Nahida','Navia','Neuvillette'
            ,'Nilou''Nigguang','Noelle','Qiqi','Raiden Shogun','Razor'
            ,'Rosaria','Sangonomiya Kokomi','Sayu','Shenhe','Shikanoin Heizou'
            ,'Sucrose','Tartagila','Thoma','Tighnari','Traveler','Venti'
            ,'Wanderer','Wriothesley','Xiangling','Xianyun','Xiao','Xingqiu'
            ,'Xinyan','Yae Miko','Yanfei','Yaoyao','Yelan','Yoimiya','Yun Jin','Zhongli']

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
      CharaChosen = ttk.Combobox(self,font = ("Times New Roman", 12),values=CharaLst,width=20,textvariable=boxvalue)
      CharaChosen.grid(column = 1, row = 2 , padx = 5, pady = 5 )
      CharaChosen.current()
      CharaChosen.bind('<KeyRelease>',search)

      #Buttons to Enter Character Names
      EnterButton = ttk.Button(self, text="ENTER", width = 8,command = CharacterDataFetch)
      EnterButton.grid(column = 2, row = 2, padx = 18, pady = 5 )

      global CharacterName
      CharacterName = tk.StringVar()
      CharacterName.set('')
      ttk.Label(self,text = "CharacterName :", font = ("Times New Roman",18)).grid(column = 0,row = 4,pady = 20)
      ttk.Label(self,textvariable = CharacterName, font = ("Times New Roman",18)).grid(column = 1,row = 4,pady = 20)

# Work In Progress
def CharacterDataFetch():
  CharacterName = 


#Search Function to Remove Unrelated Object
def search(self):
  searchvalue = self.widget.get()
  if searchvalue == '':
    CharaChosen['values'] = CharaLst

  else:
    data = []
    for item in CharaLst:
      if searchvalue.lower() in item.lower():
        data.append(item)
    
    CharaChosen['values'] = data
        
###UNUSED ATM Connect Data from SQLite3
def fetchname():
  conn = sqlite3.connect('genshindata.db')
  cur = conn.cursor()
  cur.execute("SELECT Name FROM Characterdata")
  namerows = cur.fetchall()
  
  #Global Variable Namelist to pull
  global namelist
  namelist = [list(row) for row in (namerows)]

CurrentScreen = charactersearch()
CurrentScreen.mainloop()