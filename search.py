###Testing for search function

import sqlite3 
import tkinter as tk
from tkinter import ttk

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

class charactersearch(tk.Tk):
    def __init__(self):
        
      tk.Tk.__init__(self)

      self.title('Character Search')
      self.wm_minsize(width=800,height=450)

      ttk.Label(self, text = "Select Character to show their Informations.", 
      font = ("Times New Roman", 15)).grid(column = 0, row = 1, padx = 10, pady = 15) 

      ttk.Label(self, text = "Select Character :", 
      font = ("Times New Roman", 12)).grid(column = 0, row = 2, padx = 0, pady = 5) 
        
      textn = tk.StringVar
      global CharaChosen
      CharaChosen = ttk.Combobox(self,font = ("Times New Roman", 12),values=CharaLst,width=30,textvariable=textn)
      CharaChosen.grid(column = 1, row = 2 , padx = 5, pady = 5 )
      CharaChosen.current()

      #Buttons to Enter Character Names
      EnterButton = ttk.Button(self, text="ENTER", width = 8)
      EnterButton.grid(column = 2, row = 2, padx = 18, pady = 5 )

      CharaChosen.bind('<KeyRelease>',searchs)

#Search Function to Remove Unrelated Object
def searchs(self):
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