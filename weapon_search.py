import sqlite3 
import tkinter as tk
from tkinter import ttk 
from PIL import ImageTk, Image
from ctypes import windll

#FIX BLURRY FONTS
windll.shcore.SetProcessDpiAwareness(1)

class weaponsearch(tk.Tk):
  def __init__(self):
    tk.Tk.__init__(self)

    #Main Root
    self.title('Weapon Search')
    self.geometry('1295x785')

    #Frame1 - MenuFrame
    self.MenuFrame = ttk.Frame(self)
    self.MenuFrame.grid(padx=20, pady=20)

    #Frame2 - InfoFrame
    self.InfoFrame = ttk.Frame(self)
    
    #Menu Frame Codes
    WeaponLabel = ttk.Label(self.MenuFrame,text = 'Please Choose a Weapon to Show Its Info. \n<<-- Or Use the FILTER Function on the LEFT',font = ("Arial", 12))
    WeaponLabel.grid(column = 1, row =0, padx = 15, pady = 15, sticky = 'w')

    weaponframe = ttk.LabelFrame(self.MenuFrame,text = 'Weapon Info',height = 200,width = 400)
    weaponframe.grid(column=0, row=0, padx=15, pady=15,sticky = 'e')

    #Sets the Default Value of Checkbox to CHECKED
    self.swordbutton_value = tk.IntVar(value = 1)
    self.claymorebutton_value = tk.BooleanVar(value = 1)
    self.polearmbutton_value = tk.BooleanVar(value = 1)
    self.catalystbutton_value = tk.BooleanVar(value = 1)
    self.bowbutton_value = tk.BooleanVar(value = 1)

    chooseweapon = ttk.Label(weaponframe, text='Select Your Weapon Type',width= 30)
    chooseweapon.grid(column=0, row=0, padx = 10,pady = 5)

    #Checkbox for WEAPON TYPES
    swordtype = ttk.Checkbutton(weaponframe,text = 'Sword',variable=self.swordbutton_value)
    swordtype.grid(column=0,row=1,sticky = 'w',padx = 10)

    claymoretype = ttk.Checkbutton(weaponframe,text = 'Claymore',variable=self.claymorebutton_value)
    claymoretype.grid(column=0,row=2,sticky = 'w',padx = 10)

    polearmtype = ttk.Checkbutton(weaponframe,text = 'Polearm',variable=self.polearmbutton_value)
    polearmtype.grid(column=0,row=3,sticky = 'w',padx = 10)

    catalysttype = ttk.Checkbutton(weaponframe,text = 'Catalyst',variable=self.catalystbutton_value)
    catalysttype.grid(column=0,row=4,sticky = 'w',padx = 10)

    bowtype = ttk.Checkbutton(weaponframe,text = 'Bow',variable=self.bowbutton_value)
    bowtype.grid(column=0,row=5,sticky = 'w',padx = 10)

    #Create a scrollable frame
    self.scrollable_frame = ttk.Frame(self.MenuFrame)
    self.scrollable_frame.grid(columnspan = 2,column = 0,row = 2,sticky='w',padx = 22)

    #Create a scrollbar
    self.scrollbar = ttk.Scrollbar(self.scrollable_frame, orient=tk.VERTICAL)
    self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    #Create a canvas
    self.canvas = tk.Canvas(self.scrollable_frame, yscrollcommand=self.scrollbar.set,width = 1200)
    self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    self.scrollbar.config(command=self.canvas.yview)

    #Create a frame inside the canvas to hold the images
    self.image_frame = ttk.Frame(self.canvas)
    self.canvas.create_window((0, 0), window=self.image_frame, anchor='nw')

    #Adds images to the frame
    self.fetchname()
    
    ###UNUSED CODE
    images = [f"Weapon_{i}.png" for i in imagenamelist]

    self.add_images(images)

    #Configure canvas scroll region
    self.canvas.bind("<Configure>", self.on_canvas_configure)

    self.show_MenuFrame()

    #Frame 2 Codes
    self.switch_button = ttk.Button(self.InfoFrame, text="Switch Frames", command= self.switch_frames)
    self.switch_button.grid(padx=20, pady=10)

  def add_images(self,images):
    for i, name in enumerate(imagenamelist):
      row = i // 7  # 7 images per row
      col = i % 7
      weaponname = namelist[i]
      currentname = name

      label = ttk.Label(self.image_frame)
      label.grid(row=row, column=col, padx=10, pady=10)
      label.bind("<Button-1>", self.ImageClicked)

      row = row+1
      label2 = ttk.Label(self.image_frame,text = weaponname)
      label2.grid(row=row, column=col, padx=10)

      #Insert Image of Weapon
      image_path = f"Genshin_Weapon_Image/Weapon_{currentname}.png"
      image = Image.open(image_path)
      resized_image = image.resize((128, 128))
      charphoto = ImageTk.PhotoImage(resized_image)
      label.config(image=charphoto)
      label.image = charphoto

  def on_canvas_configure(self, event):
    self.canvas.configure(scrollregion=self.canvas.bbox("all"))

  def fetchname(self):
    conn = sqlite3.connect('genshindata.db')
    cur = conn.cursor()
    cur.execute("SELECT ImgName FROM WeaponData")
    namerows = cur.fetchall()
    global imagenamelist
    imagenamelist = [row[0] for row in namerows]
    imagenamelist.sort()

    cur.execute("SELECT Name FROM WeaponData")
    namerows = cur.fetchall()
    global namelist
    namelist = [row[0] for row in namerows]
    namelist.sort()

    conn.close()

  def ImageClicked(self,event):
    if self.current_frame == self.MenuFrame:
      self.show_InfoFrame()
    else:
      self.show_MenuFrame()

  def show_MenuFrame(self):
    self.current_frame = self.MenuFrame
    self.MenuFrame.grid()
    self.InfoFrame.grid_forget()

  def show_InfoFrame(self):
    self.current_frame = self.InfoFrame
    self.InfoFrame.grid()
    self.MenuFrame.grid_forget()

  def switch_frames(self):
    if self.current_frame == self.MenuFrame:
        self.show_InfoFrame()
    else:
        self.show_MenuFrame()

CurrentScreen = weaponsearch()
CurrentScreen.mainloop()