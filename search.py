###Testing for search function

import sqlite3 
import tkinter as tk
from tkinter import ttk

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

class search(tk.Tk):
    def __init__(self):
        
        tk.Tk.__init__(self)

        self.title('Character Search')
        self.wm_minsize(width=800,height=450)

        ttk.Label(self, text = "Select Character :", 
          font = ("Times New Roman", 15)).grid(column = 0, 
          row = 5, padx = 10, pady = 25) 
        
        #Retrieve Names
        fetchname()
        
        textn = tk.StringVar
        CharaChosen = ttk.Combobox(self,values=namelist,width=30,textvariable=textn)
        CharaChosen.grid(column = 1, row = 5 , padx=10, pady=25 )
        CharaChosen.current()
    
def fetchname():
  conn = sqlite3.connect('genshindata.db')
  cur = conn.cursor()
  cur.execute("SELECT Name FROM Characterdata")
  namerows = cur.fetchall()
  
  #Global Variable Namelist to pull
  global namelist
  namelist = [list(row) for row in namerows]

CurrentScreen = search()
CurrentScreen.mainloop()