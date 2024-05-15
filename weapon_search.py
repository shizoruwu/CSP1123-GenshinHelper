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
    self.geometry('1310x825')

    #Frame1 - MenuFrame
    self.MenuFrame = ttk.Frame(self)
    self.MenuFrame.grid(padx=20, pady=20)

    #Frame2 - InfoFrame
    self.InfoFrame = ttk.Frame(self)
    
    #Menu Frame Codes
    WeaponLabel = ttk.Label(self.MenuFrame,justify='center',text = 'Please Choose a Weapon to Show Its Info. \n<<-- Or Use the FILTER Function on the LEFT',font = ("Arial", 12))
    WeaponLabel.grid(column = 2, row =0, padx = 8, pady = 15, sticky = 'nw')

    weaponframe = ttk.LabelFrame(self.MenuFrame,text = 'Weapon Type',height = 220,width = 300)
    weaponframe.grid(column=0, row=0, padx=8, pady=15,sticky = 'nw')

    qualityframe = ttk.LabelFrame(self.MenuFrame,text = 'Weapon Quality',height = 220,width = 300)
    qualityframe.grid(column=1, row=0, padx=8, pady=15,sticky = 'nw')

    self.weaponimage = ttk.LabelFrame(self.MenuFrame,text = 'Weapon List',width = 1240,height = 500)
    self.weaponimage.grid(columnspan=3,column=0,row=1)

    #Sets the Default Value of Checkbox to CHECKED
    self.swordbutton_value = tk.BooleanVar(value = 1)
    self.claymorebutton_value = tk.BooleanVar(value = 1)
    self.polearmbutton_value = tk.BooleanVar(value = 1)
    self.catalystbutton_value = tk.BooleanVar(value = 1)
    self.bowbutton_value = tk.BooleanVar(value = 1)

    self.fivestarbutton_value = tk.BooleanVar(value = 1)
    self.fourstarbutton_value = tk.BooleanVar(value = 1)
    self.otherstarbutton_value = tk.BooleanVar(value = 1)

    chooseweapon = ttk.Label(weaponframe, text='Select Your Weapon Type',width= 30)
    chooseweapon.grid(column=0, row=0, padx = 10,pady = 5)

    #Checkbox for WEAPON TYPES
    swordtype = ttk.Checkbutton(weaponframe,text = 'Sword',variable=self.swordbutton_value , command=self.add_images_filtered)
    swordtype.grid(column=0,row=1,sticky = 'w',padx = 10)

    claymoretype = ttk.Checkbutton(weaponframe,text = 'Claymore',variable=self.claymorebutton_value,command=self.add_images_filtered)
    claymoretype.grid(column=0,row=2,sticky = 'w',padx = 10)

    polearmtype = ttk.Checkbutton(weaponframe,text = 'Polearm',variable=self.polearmbutton_value,command=self.add_images_filtered)
    polearmtype.grid(column=0,row=3,sticky = 'w',padx = 10)

    catalysttype = ttk.Checkbutton(weaponframe,text = 'Catalyst',variable=self.catalystbutton_value,command=self.add_images_filtered)
    catalysttype.grid(column=0,row=4,sticky = 'w',padx = 10)

    bowtype = ttk.Checkbutton(weaponframe,text = 'Bow',variable=self.bowbutton_value,command=self.add_images_filtered)
    bowtype.grid(column=0,row=5,sticky = 'w',padx = 10)

    #Checkbox for Weapon QUALITY FILTER

    choosequality = ttk.Label(qualityframe, text='Select Your Weapon Quality',width= 30)
    choosequality.grid(column=0, row=0, padx = 10,pady = 5)

    five_star = ttk.Checkbutton(qualityframe,text = '5 STAR Weapon',variable=self.fivestarbutton_value , command=self.add_images_filtered)
    five_star.grid(column=0,row=1,sticky = 'w',padx = 10)

    four_star = ttk.Checkbutton(qualityframe,text = '4 STAR Weapon',variable=self.fourstarbutton_value , command=self.add_images_filtered)
    four_star.grid(column=0,row=2,sticky = 'w',padx = 10)

    four_star = ttk.Checkbutton(qualityframe,text = '3 STAR & Below Weapon',variable=self.otherstarbutton_value , command=self.add_images_filtered)
    four_star.grid(column=0,row=3,sticky = 'w',padx = 10)

    #Create a scrollable frame
    self.scrollable_frame = ttk.Frame(self.weaponimage)
    self.scrollable_frame.grid(column = 0,row = 0,sticky='w',padx = 10)

    #Create a scrollbar
    self.scrollbar = ttk.Scrollbar(self.scrollable_frame, orient=tk.VERTICAL)
    self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    #Create a canvas
    self.canvas = tk.Canvas(self.scrollable_frame, yscrollcommand=self.scrollbar.set,width = 1220,height = 480)
    self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    self.scrollbar.config(command=self.canvas.yview)

    #Create a frame inside the canvas
    self.image_frame = ttk.Frame(self.canvas)
    self.canvas.create_window((0, 0), window=self.image_frame, anchor='nw')

    #Adds images to the frame
    self.fetchname()
    self.add_images()

    #Configure canvas scroll region
    self.canvas.bind("<Configure>", self.on_canvas_configure)

    self.show_MenuFrame()

    #Frame 2 Codes
    self.switch_button = ttk.Button(self.InfoFrame, text="Back", command= self.switch_frames)
    self.switch_button.grid(padx=20, pady=10)

  #Add image Functions
  def add_images(self):
    for i, name in enumerate(imagenamelist_sort):
      row = i // 7  # 7 images per row
      if row != 0:
        row = row*2
      col = i % 7
      weaponname = namelist_sort[i]
      currentname = name

      label = ttk.Label(self.image_frame,width = 160,justify='center')
      label.grid(row=row, column=col, padx=10, pady=10,sticky='n')
      label.bind("<Button-1>",lambda event, clickedname = weaponname: self.ImageClicked(event,clickedname))

      row = row+1
      label2 = ttk.Label(self.image_frame,justify='center',wraplength = 160,text = weaponname)
      label2.grid(row=row, column=col, padx=10,sticky = 'n')

      #Insert Image of Weapon
      image_path = f"Genshin_Weapon_Image/Weapon_{currentname}.png"
      image = Image.open(image_path)
      resized_image = image.resize((128, 128))
      charphoto = ImageTk.PhotoImage(resized_image)
      label.config(image=charphoto)
      label.image = charphoto

  def on_canvas_configure(self, event):
    self.canvas.configure(scrollregion=self.canvas.bbox("all"))

  #Fetch Names of Weapon
  def fetchname(self):
    conn = sqlite3.connect('genshindata.db')
    cur = conn.cursor()
    cur.execute("SELECT ImgName FROM WeaponData")
    namerows = cur.fetchall()
    global imagenamelist , imagenamelist_sort
    imagenamelist = [row[0] for row in namerows]
    imagenamelist_sort = [row[0] for row in namerows]
    imagenamelist_sort.sort()

    cur.execute("SELECT Name FROM WeaponData")
    namerows = cur.fetchall()
    global namelist , namelist_sort
    namelist = [row[0] for row in namerows]
    namelist_sort = [row[0] for row in namerows]
    namelist_sort.sort()

    cur.execute("SELECT Type FROM WeaponData")
    namerows = cur.fetchall()
    global weapontype
    weapontype = [row[0] for row in namerows]

    cur.execute("SELECT Quality FROM WeaponData")
    namerows = cur.fetchall()
    global weaponquality
    weaponquality = [row[0] for row in namerows]

    conn.close()

  #When Clicked , Show info (Switch Frames)
  def ImageClicked(self,event,clickedname):
    print (clickedname)
    if self.current_frame == self.MenuFrame:
      self.show_InfoFrame()
    else:
      self.show_MenuFrame()

  #Show Menu Frame Func
  def show_MenuFrame(self):
    self.current_frame = self.MenuFrame
    self.MenuFrame.grid(padx=20, pady=20)
    self.InfoFrame.grid_forget()

  #Show Info Frame Func
  def show_InfoFrame(self):
    self.current_frame = self.InfoFrame
    self.InfoFrame.grid()
    self.MenuFrame.grid_forget()

  #Switching between frames
  def switch_frames(self):
    if self.current_frame == self.MenuFrame:
      self.show_InfoFrame()
    else:
      self.show_MenuFrame()

  def add_images_filtered(self):
    #Destroy Current Frame
    self.image_frame.destroy()
    
    #Create another empty frame
    self.image_frame = ttk.Frame(self.canvas)
    self.canvas.create_window((0, 0), window=self.image_frame, anchor='nw')

    #Determined Filtered Weapon Types
    selected_types = []
    if self.swordbutton_value.get():
      selected_types.append("Sword")
    if self.claymorebutton_value.get():
      selected_types.append("Claymore")
    if self.polearmbutton_value.get():
      selected_types.append("Polearm")
    if self.catalystbutton_value.get():
      selected_types.append("Catalyst")
    if self.bowbutton_value.get():
      selected_types.append("Bow")

    selected_quality = []
    if self.fivestarbutton_value.get():
      selected_quality.append('5')
    if self.fourstarbutton_value.get():
      selected_quality.append('4')
    if self.otherstarbutton_value.get():
      selected_quality.append('3')
      selected_quality.append('2')
      selected_quality.append('1')

    filtered_name = []
    filtered_imgname = []

    #Sort Out Filtered Names
    for i, name in enumerate(imagenamelist):
      weaponname = namelist[i]
        
      currentweapontype = weapontype[i]
      currentweaponquality = weaponquality[i]

      if (currentweapontype in selected_types) and (currentweaponquality in selected_quality):
        filtered_name.append(weaponname)
        filtered_imgname.append(name)

      filtered_name.sort()
      filtered_imgname.sort()

    #Display New List of Data
    for i, name in enumerate(filtered_imgname):
      row = i // 7  # 7 images per row
      if row != 0:
        row = row*2
      col = i % 7
      weaponname = filtered_name[i]
      currentname = name

      label = ttk.Label(self.image_frame,width = 160,justify='center')
      label.grid(row=row, column=col, padx=10, pady=10,sticky='n')
      label.bind("<Button-1>",lambda event, clickedname = weaponname: self.ImageClicked(event,clickedname))

      row = row+1
      label2 = ttk.Label(self.image_frame,justify='center',wraplength = 160,text = weaponname)
      label2.grid(row=row, column=col, padx=10,sticky = 'n')

      #Insert Image of Weapon
      image_path = f"Genshin_Weapon_Image/Weapon_{currentname}.png"
      image = Image.open(image_path)
      resized_image = image.resize((128, 128))
      charphoto = ImageTk.PhotoImage(resized_image)
      label.config(image=charphoto)
      label.image = charphoto

CurrentScreen = weaponsearch()
CurrentScreen.mainloop()