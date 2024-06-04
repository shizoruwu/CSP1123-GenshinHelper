import sqlite3 
from tkinter import *
import tkinter as tk
import ttkbootstrap as ttk
from PIL import ImageTk, Image
from ctypes import windll
import webbrowser

class charsearch(ttk.LabelFrame):
    def __init__(self,master,*args,**kargs):
        super().__init__(master,*args,**kargs)

        self.master = master
        self.label = ttk.Label(text="Character Search", style="fontt.TLabel")
        self.config(labelwidget=self.label)

        #Frame1 - MenuFrame
        self.MenuFrame = ttk.Frame(self)
        self.MenuFrame.grid(column=0, row=0, sticky='w')

        #Frame2 - InfoFrame
        self.InfoFrame = ttk.Frame(self)
        
        #Menu Frame Codes
        charLabel = ttk.Label(self.MenuFrame,justify='center',text = 'Please Choose a Character By Clicking Them. \n<<-- Or Use the FILTER Function on the LEFT',font = ("Arial", 12))
        charLabel.grid(column = 2, row =0, padx = 8, pady = 15, sticky = 'nws')

        elementframe = ttk.LabelFrame(self.MenuFrame,text = 'Character Element',height = 220,width = 300)
        elementframe.grid(column=0, row=0, padx=8, pady=15,sticky = 'nw')

        starframe = ttk.LabelFrame(self.MenuFrame,text = 'Character Star',height = 220,width = 300)
        starframe.grid(column=1, row=0, padx=8, pady=15,sticky = 'nw')

        self.charimage = ttk.LabelFrame(self.MenuFrame,text = 'Character List',width = 1240,height = 500)
        self.charimage.grid(columnspan=3,column=0,row=1)

        #Sets the Default Value of Checkbox to CHECKED
        self.cryo_value = tk.BooleanVar(value = 1)
        self.dendro_value = tk.BooleanVar(value = 1)
        self.pyro_value = tk.BooleanVar(value = 1)
        self.hydro_value = tk.BooleanVar(value = 1)
        self.anemo_value = tk.BooleanVar(value = 1)
        self.electro_value = tk.BooleanVar(value = 1)
        self.geo_value = tk.BooleanVar(value = 1)

        self.fivestarbutton_value = tk.BooleanVar(value = 1)
        self.fourstarbutton_value = tk.BooleanVar(value = 1)

        chooseweapon = ttk.Label(elementframe, text="Select Your Character's Element",width= 30)
        chooseweapon.grid(columnspan = 2,column=0, row=0, padx = 10,pady = 5)

        #Checkbox for WEAPON TYPES
        cryotype = ttk.Checkbutton(elementframe,text = 'Cryo',variable=self.cryo_value , command=self.add_images_filtered)
        cryotype.grid(column=0,row=1,sticky = 'w',padx = 10)

        dendrotype = ttk.Checkbutton(elementframe,text = 'Dendro',variable=self.dendro_value,command=self.add_images_filtered)
        dendrotype.grid(column=0,row=2,sticky = 'w',padx = 10)

        pyrotype = ttk.Checkbutton(elementframe,text = 'Pyro',variable=self.pyro_value,command=self.add_images_filtered)
        pyrotype.grid(column=0,row=3,sticky = 'w',padx = 10)

        hydrotype = ttk.Checkbutton(elementframe,text = 'Hydro',variable=self.hydro_value,command=self.add_images_filtered)
        hydrotype.grid(column=0,row=4,sticky = 'w',padx = 10)

        anemotype = ttk.Checkbutton(elementframe,text = 'Anemo',variable=self.anemo_value,command=self.add_images_filtered)
        anemotype.grid(column=1,row=1,sticky = 'w',padx = 10)

        electrotype = ttk.Checkbutton(elementframe,text = 'Electro',variable=self.electro_value,command=self.add_images_filtered)
        electrotype.grid(column=1,row=2,sticky = 'w',padx = 10)

        geotype = ttk.Checkbutton(elementframe,text = 'Geo',variable=self.geo_value,command=self.add_images_filtered)
        geotype.grid(column=1,row=3,sticky = 'w',padx = 10)

        selectallbutton = ttk.Button(elementframe,text='Select All',command=self.selectallweapon)
        selectallbutton.grid(column = 0, row = 6 ,sticky = 'es',padx = 8,pady = 3)

        clearbutton = ttk.Button(elementframe,text='Clear All',command=self.clearallweapon)
        clearbutton.grid(column = 1, row = 6 ,sticky = 'ws',padx = 8,pady = 3)


        #Checkbox for Weapon QUALITY FILTER

        choosequality = ttk.Label(starframe, text="Select Your Character's Star",width= 30)
        choosequality.grid(columnspan = 2,column=0, row=0, padx = 10,pady = 5)

        five_star = ttk.Checkbutton(starframe,text = '5 STAR ',variable=self.fivestarbutton_value , command=self.add_images_filtered)
        five_star.grid(columnspan = 2,column=0,row=1,sticky = 'w',padx = 10)

        four_star = ttk.Checkbutton(starframe,text = '4 STAR ',variable=self.fourstarbutton_value , command=self.add_images_filtered)
        four_star.grid(columnspan = 2,column=0,row=2,sticky = 'w',padx = 10)

        selectallbuttonstar = ttk.Button(starframe,text='Select All',command=self.selectallstar)
        selectallbuttonstar.grid(column = 0, row = 4 ,sticky = 'es',padx = 8,pady = 8)

        clearbuttonstar = ttk.Button(starframe,text='Clear All',command=self.clearallstar)
        clearbuttonstar.grid(column = 1, row = 4 ,sticky = 'ws',padx = 8,pady = 8)

        #Create a scrollable frame
        self.scrollable_frame = ttk.Frame(self.charimage)
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
        self.add_images_filtered()

        #Configure canvas scroll region
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        self.show_MenuFrame()

        #Frame 2 Codes
        global CharName , CharElement , CharType , CharRegion , CharInfo , CharBday , CharStar

        CharName = tk.StringVar()
        CharElement = tk.StringVar()
        CharType = tk.StringVar()
        CharRegion = tk.StringVar()
        CharInfo = tk.StringVar()
        CharBday = tk.StringVar()
        CharStar = tk.StringVar()

        CharName.set(' ')
        CharElement.set(' ')
        CharType.set(' ')
        CharRegion.set(' ')
        CharInfo.set(' ')
        CharBday.set(' ')
        CharStar.set(' ')

        CharaName = ttk.Label(self.InfoFrame,text = "Character Name :" , font = ("Arial",15)).grid(column = 0,row = 4,pady = 5,sticky = 'e')
        CharaNameData = ttk.Label(self.InfoFrame,width = 36 , textvariable = CharName, font = ("Arial",15)).grid(column = 1,row = 4,padx = 15,pady = 5,sticky = 'w')

        CharacterStar = ttk.Label(self.InfoFrame,text = "Character Star :", font = ("Arial",15)).grid(column = 0,row = 5,pady = 5,sticky = 'e')
        CharaStarData = ttk.Label(self.InfoFrame,textvariable = CharStar, font = ("Arial",15)).grid(column = 1,row = 5,padx = 15,pady = 5,sticky = 'w')

        CharacterElement = ttk.Label(self.InfoFrame,text = "Character Element :", font = ("Arial",15)).grid(column = 0,row = 6,pady = 5,sticky = 'e')
        CharaElementData = ttk.Label(self.InfoFrame,textvariable = CharElement, font = ("Arial",15)).grid(column = 1,row = 6,padx = 15,pady = 5,sticky = 'w')

        CharWeapon = ttk.Label(self.InfoFrame,text = "Character Weapon :", font = ("Arial",15)).grid(column = 0,row = 7,pady = 5,sticky = 'e')
        CharWeaponData = ttk.Label(self.InfoFrame,textvariable = CharType, font = ("Arial",15)).grid(column = 1,row = 7,padx = 15,pady = 5,sticky = 'w')

        CharacterRegion = ttk.Label(self.InfoFrame,text = "Character Region :", font = ("Arial",15)).grid(column = 0,row = 8,pady = 5,sticky = 'e')
        CharRegionData = ttk.Label(self.InfoFrame,textvariable = CharRegion, font = ("Arial",15)).grid(column = 1,row = 8,padx = 15,pady = 5,sticky = 'w')
        
        CharBirthday = ttk.Label(self.InfoFrame,text = "Character Birthday :", font = ("Arial",15)).grid(column = 0,row = 9,pady = 5,sticky = 'e')
        CharBirthdayData = ttk.Label(self.InfoFrame,textvariable = CharBday, font = ("Arial",15)).grid(column = 1,row = 9,padx = 15,pady = 5,sticky = 'w')
        
        CharacterInfo = ttk.Label(self.InfoFrame,text = "Character Info :", font = ("Arial",15)).grid(column = 0,row = 10,pady = 5,sticky = 'ne')
        CharacterInfoData = ttk.Label(self.InfoFrame,textvariable = CharInfo , wraplength = 600 , font = ("Arial",12)).grid(columnspan = 2 ,column = 1,row = 10,padx = 15,pady = 5,sticky = 'w')
        
        #CharEmptyRow = ttk.Label(self.InfoFrame,text = ' ').grid(columnspan = 4 , row = 11 , pady = 60)

        global CharacterImage
        CharacterImage = ttk.Label(self.InfoFrame)
        CharacterImage.grid(column = 3,row = 3,rowspan = 10,padx = 15,pady = 15,sticky = 'nw')

        self.switch_button = ttk.Button(self.InfoFrame,width = 12, text="Back", command= self.switch_frames)
        self.switch_button.grid(columnspan=2,column=0,row=11,padx=20, pady=10,sticky = 'w')

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    #Fetch Names of Weapon
    def fetchname(self):
        conn = sqlite3.connect('genshindata.db')
        cur = conn.cursor()
        cur.execute("SELECT Name FROM Characterdata")
        namerows = cur.fetchall()
        global charnamelist , charnamelist_sort
        charnamelist = [row[0] for row in namerows]
        charnamelist_sort = [row[0] for row in namerows]
        charnamelist_sort.sort()

        cur.execute("SELECT Element FROM Characterdata")
        namerows = cur.fetchall()
        global charelement
        charelement = [row[0] for row in namerows]

        cur.execute("SELECT Star FROM Characterdata")
        namerows = cur.fetchall()
        global characterstar
        characterstar = [row[0] for row in namerows]

        conn.close()

    #When Clicked , Show info (Switch Frames)
    def imageclicked(self,event,clickedname):

        #Retrieve Data
        conn = sqlite3.connect('genshindata.db')
        cursor = conn.cursor()

        cursor.execute("SELECT Name FROM CharacterData WHERE Name = ?", (clickedname,))
        row = cursor.fetchone()
        if row:
            CharName.set(row[0])
        
        cursor.execute("SELECT Info FROM CharacterData WHERE Name = ?", (clickedname,))
        row = cursor.fetchone()
        if row:
            CharInfo.set(row[0])

        cursor.execute("SELECT Element FROM CharacterData WHERE Name = ?", (clickedname,))
        row = cursor.fetchone()
        if row:
            CharElement.set(row[0])

        cursor.execute("SELECT Star FROM CharacterData WHERE Name = ?", (clickedname,))
        row = cursor.fetchone()
        if row:
            row = row[0]
            if row == '1':
                CharStar.set('5 Star')
            else:
                CharStar.set('4 Star')
                
        cursor.execute("SELECT Birthday FROM CharacterData WHERE Name = ?", (clickedname,))
        row = cursor.fetchone()
        if row:
            CharBday.set(row[0])

        cursor.execute("SELECT WeaponType FROM CharacterData WHERE Name = ?", (clickedname,))
        row = cursor.fetchone()
        if row:
            CharType.set(row[0])

        cursor.execute("SELECT Region FROM CharacterData WHERE Name = ?", (clickedname,))
        row = cursor.fetchone()
        if row:
            CharRegion.set(row[0])

        #Switch to Info Frame
        if self.current_frame == self.MenuFrame:
            self.show_InfoFrame()
        else:
            self.show_MenuFrame()

        try:
          # Show Character Image
          image_path = f"Genshin_Image/{clickedname}_Card.png"
          image = Image.open(image_path)
          resized_image = image.resize((265, 515))
          charphoto = ImageTk.PhotoImage(resized_image)
          CharacterImage.config(image=charphoto)
          CharacterImage.image = charphoto  # Keep a reference to prevent image from being garbage collected
        except FileNotFoundError:
          print("Image not found:", image_path)

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
        global selected_quality , selected_element
        selected_element = []
        if self.dendro_value.get():
            selected_element.append("Dendro")
        if self.cryo_value.get():
            selected_element.append("Cryo")
        if self.pyro_value.get():
            selected_element.append("Pyro")
        if self.hydro_value.get():
            selected_element.append("Hydro")
        if self.anemo_value.get():
            selected_element.append("Anemo")
        if self.electro_value.get():
            selected_element.append("Electro")
        if self.geo_value.get():
            selected_element.append("Geo")

        selected_quality = []
        if self.fivestarbutton_value.get():
            selected_quality.append('1')
        if self.fourstarbutton_value.get():
            selected_quality.append('0')

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

        #Sort Out Filtered Names
        for i, name in enumerate(charnamelist):
            charname = name
                
            currentcharelement = charelement[i]
            currentcharquality = characterstar[i]

            if (currentcharelement in selected_element) and (currentcharquality in selected_quality):
                filtered_name.append(charname)

        filtered_name.sort()

        #Display New List of Data
        for i, name in enumerate(filtered_name):
            row = i // 7  # 7 images per row
            if row != 0:
                row = row*2
            col = i % 7
            charname = name

            label = ttk.Label(self.image_frame,width = 155,justify='center')
            label.grid(row=row, column=col, padx=10, pady=10,sticky='n')
            label.bind("<Button-1>",lambda event, clickedname = charname: self.imageclicked(event,clickedname))

            row = row+1
            label2 = ttk.Label(self.image_frame,justify='center',wraplength = 155,text = charname)
            label2.grid(row=row, column=col, padx=10,sticky = 'n')

            #Insert Image of Weapon
            image_path = f"Genshin_Character_Icon/ui-avataricon-{charname}.png"
            image = Image.open(image_path)
            resized_image = image.resize((145, 145))
            charphoto = ImageTk.PhotoImage(resized_image)
            label.config(image=charphoto)
            label.image = charphoto
        
    #Function for Clearing all weapon checkbox
    def clearallweapon(self):
        self.cryo_value.set(0)
        self.dendro_value.set(0)
        self.pyro_value.set(0)
        self.hydro_value.set(0)
        self.anemo_value.set(0)
        self.electro_value.set(0)
        self.geo_value.set(0)

        self.add_images_filtered()

    #Function for clearing all weapon's star checkbox
    def clearallstar(self):
        self.fivestarbutton_value.set(0)
        self.fourstarbutton_value.set(0)

        self.add_images_filtered()

    #Select all Weapon
    def selectallweapon(self):
        self.cryo_value.set(1)
        self.dendro_value.set(1)
        self.pyro_value.set(1)
        self.hydro_value.set(1)
        self.anemo_value.set(1)
        self.electro_value.set(1)
        self.geo_value.set(1)

        self.add_images_filtered()

    #Select all stars
    def selectallstar(self):
        self.fivestarbutton_value.set(1)
        self.fourstarbutton_value.set(1)

        self.add_images_filtered()

def main():
    windll.shcore.SetProcessDpiAwareness(1)

    root = ttk.Window()
    root.title("Character Search")
    root.geometry('1310x825')

    notic = charsearch(root)
    notic.grid(column=1, row=1, padx=15, pady=10, ipady=100, ipadx=250)

    root.mainloop()

if __name__ == '__main__':
    main()