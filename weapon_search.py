import sqlite3 
import tkinter as tk
import ttkbootstrap as ttk
from PIL import ImageTk, Image
from ctypes import windll
import webbrowser

#FIX BLURRY FONTS
windll.shcore.SetProcessDpiAwareness(1)

class weaponsearch(ttk.LabelFrame):
  def __init__(self,master,*args,**kargs):
    super().__init__(master,*args,**kargs)
    
    self.master = master
    self.label = ttk.Label(text="Weapon Search", style="fontt.TLabel")
    self.config(labelwidget=self.label)

    #Frame1 - MenuFrame
    self.MenuFrame = ttk.Frame(self)
    self.MenuFrame.grid(padx=20, pady=20)

    #Frame2 - InfoFrame
    self.InfoFrame = ttk.Frame(self)
    
    #Menu Frame Codes
    WeaponLabel = ttk.Label(self.MenuFrame,justify='center',text = 'Please Choose a Weapon to Show Its Info. \n<<-- Or Use the FILTER Function on the LEFT',font = ("Arial", 12))
    WeaponLabel.grid(column = 2, row =0, padx = 8, pady = 15, sticky = 'ne')

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
    chooseweapon.grid(columnspan = 2,column=0, row=0, padx = 10,pady = 5)

    #Checkbox for WEAPON TYPES
    swordtype = ttk.Checkbutton(weaponframe,text = 'Sword',variable=self.swordbutton_value , command=self.add_images_filtered)
    swordtype.grid(columnspan = 2,column=0,row=1,sticky = 'w',padx = 10)

    claymoretype = ttk.Checkbutton(weaponframe,text = 'Claymore',variable=self.claymorebutton_value,command=self.add_images_filtered)
    claymoretype.grid(columnspan = 2,column=0,row=2,sticky = 'w',padx = 10)

    polearmtype = ttk.Checkbutton(weaponframe,text = 'Polearm',variable=self.polearmbutton_value,command=self.add_images_filtered)
    polearmtype.grid(columnspan = 2,column=0,row=3,sticky = 'w',padx = 10)

    catalysttype = ttk.Checkbutton(weaponframe,text = 'Catalyst',variable=self.catalystbutton_value,command=self.add_images_filtered)
    catalysttype.grid(columnspan = 2,column=0,row=4,sticky = 'w',padx = 10)

    bowtype = ttk.Checkbutton(weaponframe,text = 'Bow',variable=self.bowbutton_value,command=self.add_images_filtered)
    bowtype.grid(columnspan = 2,column=0,row=5,sticky = 'w',padx = 10)

    selectallbutton = ttk.Button(weaponframe,text='Select All',command=self.selectallweapon)
    selectallbutton.grid(column = 0, row = 6 ,sticky = 'es',padx = 8,pady = 3)

    clearbutton = ttk.Button(weaponframe,text='Clear All',command=self.clearallweapon)
    clearbutton.grid(column = 1, row = 6 ,sticky = 'ws',padx = 8,pady = 3)


    #Checkbox for Weapon QUALITY FILTER

    choosequality = ttk.Label(qualityframe, text='Select Your Weapon Quality',width= 30)
    choosequality.grid(columnspan = 2,column=0, row=0, padx = 10,pady = 5)

    five_star = ttk.Checkbutton(qualityframe,text = '5 STAR Weapon',variable=self.fivestarbutton_value , command=self.add_images_filtered)
    five_star.grid(columnspan = 2,column=0,row=1,sticky = 'w',padx = 10)

    four_star = ttk.Checkbutton(qualityframe,text = '4 STAR Weapon',variable=self.fourstarbutton_value , command=self.add_images_filtered)
    four_star.grid(columnspan = 2,column=0,row=2,sticky = 'w',padx = 10)

    other_star = ttk.Checkbutton(qualityframe,text = '3 STAR & Below Weapon',variable=self.otherstarbutton_value , command=self.add_images_filtered)
    other_star.grid(columnspan = 2,column=0,row=3,sticky = 'w',padx = 10)

    selectallbuttonstar = ttk.Button(qualityframe,text='Select All',command=self.selectallstar)
    selectallbuttonstar.grid(column = 0, row = 4 ,sticky = 'es',padx = 8,pady = 8)

    clearbuttonstar = ttk.Button(qualityframe,text='Clear All',command=self.clearallstar)
    clearbuttonstar.grid(column = 1, row = 4 ,sticky = 'ws',padx = 8,pady = 8)

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
    global InfoName , InfoType , InfoInfo , InfoQuality , InfoBaseATK , Info2ndStat , InfoRefinementName , InfoRefinementInfo

    InfoName = tk.StringVar()
    InfoType = tk.StringVar()
    InfoInfo = tk.StringVar()
    InfoQuality = tk.StringVar()
    InfoBaseATK = tk.StringVar()
    Info2ndStat = tk.StringVar()
    InfoRefinementName = tk.StringVar()
    InfoRefinementInfo = tk.StringVar()

    InfoName.set(' ')
    InfoType.set(' ')
    InfoInfo.set(' ')
    InfoQuality.set(' ')
    InfoBaseATK.set(' ')
    Info2ndStat.set(' ')
    InfoRefinementName.set(' ')
    InfoRefinementInfo.set(' ')

    InfoLabelFrame = ttk.Labelframe(self.InfoFrame,text = "Weapon's Info")
    InfoLabelFrame.grid(column=0 , row = 0 , padx = 15 , pady = 15,sticky = 'n')

    ImageLabelFrame = ttk.Labelframe(InfoLabelFrame,text = 'Image')
    ImageLabelFrame.grid(column=0 , row = 1 , padx = 15 , pady = 15,sticky='n')

    global displaylabel
    displaylabel = ttk.Label(ImageLabelFrame)
    displaylabel.grid(column=0,row=1,padx = 20, pady = 5)
    displaylabel.bind("<Button-1>", self.open_link)

    global displaylabel2nd
    displaylabel2nd = ttk.Label(ImageLabelFrame)
    displaylabel2nd.grid(column=1,row=1,padx = 20, pady = 5)
    displaylabel2nd.bind("<Button-1>", self.open_link)

    global basename , basename2nd
    basename = tk.StringVar()
    basename2nd = tk.StringVar()

    ttk.Label(ImageLabelFrame,textvariable= basename,justify='center',font = ('Arial',11)).grid(column=0,row=0,pady=5)
    ttk.Label(ImageLabelFrame,textvariable= basename2nd,justify='center',font = ('Arial',11)).grid(column=1,row=0,pady=5)

    Name = ttk.Label(InfoLabelFrame, textvariable=InfoName, font = ('Arial',15))
    Name.grid(column=0,row=0,padx = 8 , pady = 8)

    Info = ttk.Label(InfoLabelFrame, textvariable = InfoInfo , wraplength = 370 , font = ('Arial',11))
    Info.grid(column=0,row=2,padx=5,pady=5)

    WeaponAttackLabelFrame = ttk.Labelframe(self.InfoFrame,text = "Weapon's Attack Info")
    WeaponAttackLabelFrame.grid(column=1 , row = 0, padx = 15 , pady = 15,sticky='n')

    weapontypelabel = ttk.Label(WeaponAttackLabelFrame,text="Weapon's Type:",font = ('Arial',12))
    weapontypelabel.grid(column=0,row=0,padx = 5,pady = 5,sticky = 'e')
    weapontype = ttk.Label(WeaponAttackLabelFrame,textvariable=InfoType,font = ('Arial',12))
    weapontype.grid(column=1,row=0,padx = 5,pady = 5,sticky = 'w')

    qualitylabel = ttk.Label(WeaponAttackLabelFrame,text="Weapon's Quality:",font = ('Arial',12))
    qualitylabel.grid(column=0,row=1,padx = 5,pady = 5,sticky = 'e')
    quality = ttk.Label(WeaponAttackLabelFrame,textvariable=InfoQuality,font = ('Arial',12))
    quality.grid(column=1,row=1,padx = 5,pady = 5,sticky = 'w')

    baseatklabel = ttk.Label(WeaponAttackLabelFrame,text="Weapon's Base Attack:",font = ('Arial',12))
    baseatklabel.grid(column=0,row=2,padx = 5,pady = 5,sticky = 'e')
    baseatk = ttk.Label(WeaponAttackLabelFrame,textvariable=InfoBaseATK,font = ('Arial',12))
    baseatk.grid(column=1,row=2,padx = 5,pady = 5,sticky = 'w')

    seconstatlabel = ttk.Label(WeaponAttackLabelFrame,text="Weapon's Secondary Stat:",font = ('Arial',12))
    seconstatlabel.grid(column=0,row=3,padx = 5,pady = 5,sticky = 'e')
    seconstat = ttk.Label(WeaponAttackLabelFrame,textvariable=Info2ndStat,font = ('Arial',12))
    seconstat.grid(column=1,row=3,padx = 5,pady = 5,sticky = 'w')

    refinementlabel = ttk.Label(WeaponAttackLabelFrame,text="Weapon's Refinement:",font = ('Arial',12))
    refinementlabel.grid(column=0,row=4,padx = 5,pady = 5,sticky = 'e')
    refinement = ttk.Label(WeaponAttackLabelFrame,textvariable=InfoRefinementName,font = ('Arial',12))
    refinement.grid(column=1,row=4,padx = 5,pady = 5,sticky = 'w')

    refinementinfo = ttk.Label(WeaponAttackLabelFrame,textvariable=InfoRefinementInfo,font = ('Arial',10),wraplength=370)
    refinementinfo.grid(column=1,row=5,padx = 5,pady = 5,sticky = 'w')

    self.switch_button = ttk.Button(self.InfoFrame,width = 12, text="Back", command= self.switch_frames)
    self.switch_button.grid(columnspan=2,column=0,row=1,padx=20, pady=10,sticky = 'w')

  #Add image Functions
  def add_images(self):
    for i, name in enumerate(imagenamelist_sort):
      row = i // 7  # 7 images per row
      if row != 0:
        row = row*2
      col = i % 7
      weaponname = namelist_sort[i]
      currentname = name

      label = ttk.Label(self.image_frame,width = 155,justify='center')
      label.grid(row=row, column=col, padx=10, pady=10,sticky='n')
      label.bind("<Button-1>",lambda event, clickedname = weaponname: self.imageclicked(event,clickedname))

      row = row+1
      label2 = ttk.Label(self.image_frame,justify='center',wraplength = 155,text = weaponname)
      label2.grid(row=row, column=col, padx=10,sticky = 'n')

      #Insert Image of Weapon
      image_path = f"Genshin_Weapon_Image/Weapon_{currentname}.png"
      image = Image.open(image_path)
      resized_image = image.resize((145, 145))
      weapphoto = ImageTk.PhotoImage(resized_image)
      label.config(image=weapphoto)
      label.image = weapphoto

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
  def imageclicked(self,event,clickedname):

    #Retrieve Data
    conn = sqlite3.connect('genshindata.db')
    cursor = conn.cursor()

    cursor.execute("SELECT Name FROM WeaponData WHERE Name = ?", (clickedname,))
    row = cursor.fetchone()
    if row:
      InfoName.set(row[0])

    cursor.execute("SELECT ImgName FROM WeaponData WHERE Name = ?", (clickedname,))
    row = cursor.fetchone()
    if row:
      currentname = row[0]

    global url 
    if currentname == "'Ultimate_Overlord's_Mega_Magic_Sword'" or currentname == "'The_Catch'":
      url = f'https://genshin-impact.fandom.com/wiki/{clickedname}'
    else:
      url = f'https://genshin-impact.fandom.com/wiki/{currentname}'

    image_path = f"Genshin_Weapon_Image/Weapon_{currentname}.png"
    image = Image.open(image_path)
    resized_image = image.resize((145, 145))
    weapphoto = ImageTk.PhotoImage(resized_image)
    displaylabel.config(image=weapphoto,)
    displaylabel.image = weapphoto

    image_path = f"Genshin_Weapon_Image/Weapon_{currentname}_2nd.png"
    image = Image.open(image_path)
    resized_image = image.resize((145, 145))
    weapphoto = ImageTk.PhotoImage(resized_image)
    displaylabel2nd.config(image=weapphoto,)
    displaylabel2nd.image = weapphoto

    if clickedname == 'Sword of Narzissenkreuz':
      basename.set('Pneuma Form')
      basename2nd.set('Ousia Form')
    else:
      basename.set('Base')
      basename2nd.set('2nd Ascension')
    
    cursor.execute("SELECT Info FROM WeaponData WHERE Name = ?", (clickedname,))
    row = cursor.fetchone()
    if row:
      InfoInfo.set(row[0])

    cursor.execute("SELECT Type FROM WeaponData WHERE Name = ?", (clickedname,))
    row = cursor.fetchone()
    if row:
      InfoType.set(row[0])

    cursor.execute("SELECT Quality FROM WeaponData WHERE Name = ?", (clickedname,))
    row = cursor.fetchone()
    if row:
      row = f'{row[0]} Star'
      InfoQuality.set(row)

    cursor.execute("SELECT BaseAtk FROM WeaponData WHERE Name = ?", (clickedname,))
    row = cursor.fetchone()
    if row:
      InfoBaseATK.set(row[0])

    cursor.execute("SELECT SecondStat FROM WeaponData WHERE Name = ?", (clickedname,))
    row = cursor.fetchone()
    if row:
      Info2ndStat.set(row[0])

    cursor.execute("SELECT RefinementName FROM WeaponData WHERE Name = ?", (clickedname,))
    row = cursor.fetchone()
    if row:
      InfoRefinementName.set(row[0])

    cursor.execute("SELECT RefinementInfo FROM WeaponData WHERE Name = ?", (clickedname,))
    row = cursor.fetchone()
    if row:
      if (row[0]) == 'None':
        InfoRefinementInfo.set(' ')
      else:
        InfoRefinementInfo.set(row[0])

    #Switch to Info Frame
    if self.current_frame == self.MenuFrame:
      self.show_InfoFrame()
    else:
      self.show_MenuFrame()

  #Show Menu Frame Func
  def show_MenuFrame(self):
    self.current_frame = self.MenuFrame
    self.MenuFrame.grid(padx=20, pady=8)
    self.InfoFrame.grid_forget()

  #Show Info Frame Func
  def show_InfoFrame(self):
    self.current_frame = self.InfoFrame
    self.InfoFrame.grid(padx=20, pady=8)
    self.MenuFrame.grid_forget()

  #Switching between frames
  def switch_frames(self):
    if self.current_frame == self.MenuFrame:
      self.show_InfoFrame()
    else:
      self.show_MenuFrame()

  #Functions to sort out selected filters 
  def filterfunc(self):
    #Determined Filtered Weapon Types
    global selected_quality , selected_types
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

  #Function for adding in images , but with filter
  def add_images_filtered(self):
    #Destroy Current Frame
    self.image_frame.destroy()
    
    #Create another empty frame
    self.image_frame = ttk.Frame(self.canvas)
    self.canvas.create_window((0, 0), window=self.image_frame, anchor='nw')

    #Determine Filtered Info
    self.filterfunc()

    #Placeholder for Filtered Data
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

      label = ttk.Label(self.image_frame,width = 155,justify='center')
      label.grid(row=row, column=col, padx=10, pady=10,sticky='n')
      label.bind("<Button-1>",lambda event, clickedname = weaponname: self.imageclicked(event,clickedname))

      row = row+1
      label2 = ttk.Label(self.image_frame,justify='center',wraplength = 155,text = weaponname)
      label2.grid(row=row, column=col, padx=10,sticky = 'n')

      #Insert Image of Weapon
      image_path = f"Genshin_Weapon_Image/Weapon_{currentname}.png"
      image = Image.open(image_path)
      resized_image = image.resize((145, 145))
      weapphoto = ImageTk.PhotoImage(resized_image)
      label.config(image=weapphoto,)
      label.image = weapphoto

    #clear all functions
  
  #Function for Clearing all weapon checkbox
  def clearallweapon(self):
    self.swordbutton_value.set(0)
    self.claymorebutton_value.set(0)
    self.polearmbutton_value.set(0)
    self.catalystbutton_value.set(0)
    self.bowbutton_value.set(0)

    self.add_images_filtered()

  #Function for clearing all weapon's star checkbox
  def clearallstar(self):
    self.fivestarbutton_value.set(0)
    self.fourstarbutton_value.set(0)
    self.otherstarbutton_value.set(0)

    self.add_images_filtered()

  #Select all Weapon
  def selectallweapon(self):
    self.swordbutton_value.set(1)
    self.claymorebutton_value.set(1)
    self.polearmbutton_value.set(1)
    self.catalystbutton_value.set(1)
    self.bowbutton_value.set(1)

    self.add_images_filtered()

  #Select all stars
  def selectallstar(self):
    self.fivestarbutton_value.set(1)
    self.fourstarbutton_value.set(1)
    self.otherstarbutton_value.set(1)

    self.add_images_filtered()

  #QOL Feature, Opens up webpage when clicked on image for more details
  def open_link(self,event):
    webbrowser.open(url)

def main():
    windll.shcore.SetProcessDpiAwareness(1)

    root = ttk.Window()
    root.title("Character Search")
    root.geometry('1310x825')

    notic = weaponsearch(root)
    notic.grid(column=1, row=1, padx=15, pady=10, ipady=100, ipadx=250)

    root.mainloop()

if __name__ == '__main__':
    main()