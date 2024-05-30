import sqlite3
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

#def
def fetchname():   #fetch name from data base
  conn = sqlite3.connect('genshindata.db')
  cur = conn.cursor()
  cur.execute("SELECT Name FROM CharacterLevel")
  namerows = cur.fetchall()

  global namelist
  namelist = [row[0] for row in namerows]
  namelist.sort()

  conn.close()

fetchname()

#Search Function to Remove Unrelated Object
def Search(event=None):
  searchvalue = CharaChosen.get().lower()
  matching_names = [name for name in namelist if searchvalue in name.lower()]
  CharaChosen['values'] = matching_names

#clear content inside frame2 
def clear_frame():
    for widget in frame2.winfo_children():
        widget.destroy()

def frame():
  clear_frame()
  conn = sqlite3.connect('genshindata.db')
  cur = conn.cursor()
  currentname = CharaChosen.get()

  if currentname in namelist:
    #normal boss
    cur.execute("SELECT normal_boss FROM CharacterLevel WHERE Name = ?", (currentname,))
    row = cur.fetchone()
    if row:
      normal_boss.set(row[0])

    #ascension
    cur.execute("SELECT ascension FROM CharacterLevel WHERE Name = ?", (currentname,))
    row = cur.fetchone()
    if row:
      ascension.set(row[0])

    cur.execute("SELECT enhancement FROM CharacterLevel where Name = ?", (currentname,))
    row = cur.fetchone()
    if row:
      enhancement.set(row[0])

    cur.execute("SELECT flower FROM CharacterLevel where Name = ?", (currentname,))
    row = cur.fetchone()
    if row:
      flower.set(row[0])

    #current level and level wanted to be upgrade to
    curlevel = ["1", "20★", "40★", "50★", "60★", "70★", "80★"]
    sellevel = ["20★", "40★", "50★", "60★", "70★", "80★"]

    current_level = tk.StringVar()
    selected_level = tk.StringVar()
    
    curlevel_combo = ttk.Combobox(frame1, textvariable=current_level, values=curlevel)
    curlevel_combo.place(x = frame1_width + 330, y = frame1_height + 50)
    sellevel_combo = ttk.Combobox(frame1, textvariable=selected_level, values=sellevel)
    sellevel_combo.place(x = frame1_width + 630, y = frame1_height + 50)
    arrow = tk.Label(frame1, text="→", font=('Arial', 20))
    arrow.place(x = frame1_width + 560, y = frame1_height + 37)

    def combobox_selection(event):
      curlevel_value = curlevel_combo.get()
      sellevel_value = sellevel_combo.get()
      
      gemstone_value = 6
      chunk_value = 9
      fragment_value = 9
      sliver_value = 1
      enhan1_value = 18
      enhan2_value = 30
      enhan3_value = 36
      normalboss_value = 46
      flower_value = 168

      if curlevel_value == "1":
        pass
      elif curlevel_value == "20★":
        sliver_value -= 1
        flower_value -= 3
        enhan1_value -= 3

      elif curlevel_value == "40★":
        sliver_value -= 1
        fragment_value -= 3
        enhan1_value -= 18
        normalboss_value -= 2
        flower_value -= 13
      
      elif curlevel_value == "50★":
        sliver_value -= 1
        fragment_value -= 9
        enhan1_value -= 18
        enhan2_value -= 12
        normalboss_value -= 6
        flower_value -= 33

      elif curlevel_value == "60★":
        sliver_value -= 1
        fragment_value -= 9
        chunk_value -= 3
        enhan1_value -= 18
        enhan2_value -= 30
        normalboss_value -= 14
        flower_value -= 63

      elif curlevel_value == "70★":
        sliver_value -= 1
        fragment_value -= 9
        chunk_value -= 9
        enhan1_value -= 18
        enhan2_value -= 30
        enhan3_value -= 12
        normalboss_value -= 26
        flower_value -= 108

      elif curlevel_value == "80★":
        sliver_value -= 1
        fragment_value -= 9
        chunk_value -= 9
        gemstone_value -= 6
        enhan1_value -= 18
        enhan2_value -= 30
        enhan3_value -= 36
        normalboss_value -= 46
        flower_value -= 168
      
      else:
        gemstone_value = 0
        chunk_value = 0
        fragment_value = 0
        sliver_value = 0
        enhan1_value = 0
        enhan2_value = 0
        enhan3_value = 0
        normalboss_value = 0
        flower_value = 0

      gemstone_value = gemstone_value
      chunk_value = chunk_value
      fragment_value = fragment_value
      sliver_value = sliver_value
      enhan1_value = enhan1_value
      enhan2_value = enhan2_value
      enhan3_value = enhan3_value
      normalboss_value = normalboss_value
      flower_value = flower_value

      if sellevel_value == "20★":
        fragment_value -= 9
        chunk_value -= 9
        gemstone_value -= 6
        enhan1_value -= 15
        enhan2_value -= 30
        enhan3_value -= 36
        normalboss_value -= 46
        flower_value -= 165

      elif sellevel_value == "40★":
        fragment_value -= 6
        chunk_value -= 9
        gemstone_value -= 6
        enhan2_value -= 30
        enhan3_value -= 36
        normalboss_value -= 44
        flower_value -= 155

      elif sellevel_value == "50★":
        chunk_value -= 9
        gemstone_value -= 6
        enhan2_value -= 18
        enhan3_value -= 36
        normalboss_value -= 40
        flower_value -= 135

      elif sellevel_value == "60★":
        chunk_value -= 6
        gemstone_value -= 6
        enhan3_value -= 36
        normalboss_value -= 32
        flower_value -= 105

      elif sellevel_value == "70★":
        gemstone_value -= 6
        enhan3_value -= 24
        normalboss_value -= 20
        flower_value -= 60

      elif sellevel_value == "80★":
        pass

      #take only number  
      curnumber = int(curlevel_combo.get().replace("★", ""))
      selnumber = int(sellevel_combo.get().replace("★", ""))

      if selnumber <= curnumber:
        gemstone_value = 0
        chunk_value = 0
        fragment_value = 0
        sliver_value = 0
        enhan1_value = 0
        enhan2_value = 0
        enhan3_value = 0
        normalboss_value = 0
        flower_value = 0
          
      gemstone.config(text=f"x{gemstone_value}")
      chunk.config(text=f"x{chunk_value}")
      fragment.config(text=f"x{fragment_value}")
      sliver.config(text=f"x{sliver_value}")
      enhan1.config(text=f"x{enhan1_value}")
      enhan2.config(text=f"x{enhan2_value}")
      enhan3.config(text=f"x{enhan3_value}")
      normalboss.config(text=f"x{normalboss_value}")
      flowers.config(text=f"x{flower_value}")

    curlevel_combo.bind("<<ComboboxSelected>>", combobox_selection)
    sellevel_combo.bind("<<ComboboxSelected>>", combobox_selection)

    global character_image, normal_boss_image
    character_image = ttk.Label(frame2)
    character_image.grid(row = 1, column = 0, rowspan = 6, sticky = 'w')

    gemstone_image = ttk.Label(frame2)
    gemstone_image.grid(row = 0, column = 4, columnspan=2)

    gemstone = tk.Label(frame2, text="x0", font=('Arial', 10))
    gemstone.grid(row = 1, column = 4, columnspan=2, sticky = 's')

    chunk_image = ttk.Label(frame2)
    chunk_image.grid(row = 0, column = 3, columnspan=2)

    chunk = tk.Label(frame2, text="x0", font=('Arial', 10))
    chunk.grid(row = 1, column = 3, columnspan=2, sticky = 's')

    fragment_image = ttk.Label(frame2)
    fragment_image.grid(row = 0, column = 2, columnspan=2)

    fragment = tk.Label(frame2, text="x0", font=('Arial', 10))
    fragment.grid(row = 1, column = 2, columnspan=2, sticky = 's')

    sliver_image = ttk.Label(frame2)
    sliver_image.grid(row = 0, column = 1, columnspan=2)

    sliver = tk.Label(frame2, text="x0", font=('Arial', 10))
    sliver.grid(row = 1, column = 1, columnspan=2, sticky = 's')

    enhan1_image = ttk.Label(frame2)
    enhan1_image.grid(row = 2, column = 1)

    enhan1 = tk.Label(frame2, text="x0", font=('Arial', 10))
    enhan1.grid(row = 3, column = 1, sticky = 's')

    enhan2_image = ttk.Label(frame2)
    enhan2_image.grid(row = 2, column = 2)

    enhan2 = tk.Label(frame2, text="x0", font=('Arial', 10))
    enhan2.grid(row = 3, column = 2, sticky = 's')

    enhan3_image = ttk.Label(frame2)
    enhan3_image.grid(row = 2, column = 3)

    enhan3 = tk.Label(frame2, text="x0", font=('Arial', 10))
    enhan3.grid(row = 3, column = 3, sticky = 's')

    flower_image = ttk.Label(frame2)
    flower_image.grid(row = 2, column = 4)

    flowers = tk.Label(frame2, text="x0", font=('Arial', 10))
    flowers.grid(row = 3, column = 4, sticky = 's')

    normal_boss_image = ttk.Label(frame2)
    normal_boss_image.grid(row = 2, column = 5)

    normalboss = tk.Label(frame2, text="x0", font=('Arial', 10))
    normalboss.grid(row = 3, column = 5, sticky = 's')

    #pull image inside
    image_path_1 = f"Genshin_Image/{currentname}_Card.png"
    image_1 = Image.open(image_path_1)
    resized_image_1 = image_1.resize((265, 515))
    charphoto = ImageTk.PhotoImage(resized_image_1)
    character_image.config(image=charphoto)
    character_image.image = charphoto
    
    character_name = tk.Label(frame2, text=currentname, font=('Arial', 20))
    character_name.grid(row = 0, column = 0) 

    image_path_2 = f"Materials/ascension/{ascension.get()} Gemstone.png"
    image_2 = Image.open(image_path_2)
    resized_image_2 = image_2.resize((100,100))
    gemphoto = ImageTk.PhotoImage(resized_image_2)
    gemstone_image.config(image=gemphoto)
    gemstone_image.image = gemphoto

    gemstone_name = tk.Label(frame2, text = f'{ascension.get()} Gemstone', font=('Arial', 10), wraplength=100)
    gemstone_name.grid(row = 1, column = 4, columnspan=2, sticky = 'n')

    image_path_3 = f"Materials/ascension/{ascension.get()} Chunk.png"
    image_3 = Image.open(image_path_3)
    resized_image_3 = image_3.resize((100,100))
    chunkphoto = ImageTk.PhotoImage(resized_image_3)
    chunk_image.config(image=chunkphoto)
    chunk_image.image = chunkphoto

    chunk_name = tk.Label(frame2, text = f'{ascension.get()} Chunk', font=('Arial', 10), wraplength=100)
    chunk_name.grid(row = 1, column = 3, columnspan=2, sticky = 'n')   #, padx=10, pady=(25,0))

    image_path_4 = f"Materials/ascension/{ascension.get()} Fragment.png"
    image_4 = Image.open(image_path_4)
    resized_image_4 = image_4.resize((100,100))
    fragphoto = ImageTk.PhotoImage(resized_image_4)
    fragment_image.config(image=fragphoto)
    fragment_image.image = fragphoto

    frag_name = tk.Label(frame2, text = f'{ascension.get()} Fragment', font=('Arial', 10), wraplength=100)
    frag_name.grid(row = 1, column = 2, columnspan=2, sticky = 'n')   #, padx=10, pady=(25,0))

    image_path_5 = f"Materials/ascension/{ascension.get()} Sliver.png"
    image_5 = Image.open(image_path_5)
    resized_image_5 = image_5.resize((100,100))
    sliphoto = ImageTk.PhotoImage(resized_image_5)
    sliver_image.config(image=sliphoto)
    sliver_image.image = sliphoto

    sliver_name = tk.Label(frame2, text = f'{ascension.get()} Sliver', font=('Arial', 10), wraplength=100)
    sliver_name.grid(row = 1, column = 1, columnspan=2, sticky = 'n')

    if enhancement.get() == "1":
      #'Divining Scroll, Sealed Scroll, Forbidden Curse Scroll'
      image_path_6 = f"Materials/enhancement/Divining Scroll.png"
      image_6 = Image.open(image_path_6)
      resized_image_6 = image_6.resize((100,100))
      enhan1photo = ImageTk.PhotoImage(resized_image_6)
      enhan1_image.config(image=enhan1photo)
      enhan1_image.image = enhan1photo

      enhan1_name = tk.Label(frame2, text = 'Divining Scroll', font=('Arial', 10), wraplength=100)
      enhan1_name.grid(row = 3, column = 1, sticky = 'n')

      image_path_7 = f"Materials/enhancement/Sealed Scroll.png"
      image_7 = Image.open(image_path_7)
      resized_image_7 = image_7.resize((100,100))
      enhan2photo = ImageTk.PhotoImage(resized_image_7)
      enhan2_image.config(image=enhan2photo)
      enhan2_image.image = enhan2photo

      enhan2_name = tk.Label(frame2, text = 'Sealed Scroll', font=('Arial', 10), wraplength=100)
      enhan2_name.grid(row = 3, column = 2, sticky = 'n')

      image_path_8 = f"Materials/enhancement/Forbidden Curse Scroll.png"
      image_8 = Image.open(image_path_8)
      resized_image_8 = image_8.resize((100,100))
      enhan3photo = ImageTk.PhotoImage(resized_image_8)
      enhan3_image.config(image=enhan3photo)
      enhan3_image.image = enhan3photo

      enhan3_name = tk.Label(frame2, text = 'Forbidden Curse Scroll', font=('Arial', 10), wraplength=100)
      enhan3_name.grid(row = 3, column = 3, sticky = 'n')

    if enhancement.get() == "2":
      #'Faded Red Satin, Trimmed Red Silk, Rich Red Brocade'
      image_path_6 = f"Materials/enhancement/Faded Red Satin.png"
      image_6 = Image.open(image_path_6)
      resized_image_6 = image_6.resize((100,100))
      enhan1photo = ImageTk.PhotoImage(resized_image_6)
      enhan1_image.config(image=enhan1photo)
      enhan1_image.image = enhan1photo

      enhan1_name = tk.Label(frame2, text = 'Faded Red Satin', font=('Arial', 10), wraplength=100)
      enhan1_name.grid(row = 3, column = 1, sticky = 'n')

      image_path_7 = f"Materials/enhancement/Trimmed Red Silk.png"
      image_7 = Image.open(image_path_7)
      resized_image_7 = image_7.resize((100,100))
      enhan2photo = ImageTk.PhotoImage(resized_image_7)
      enhan2_image.config(image=enhan2photo)
      enhan2_image.image = enhan2photo

      enhan2_name = tk.Label(frame2, text = 'Trimmed Red Silk', font=('Arial', 10), wraplength=100)
      enhan2_name.grid(row = 3, column = 2, sticky = 'n')

      image_path_8 = f"Materials/enhancement/Rich Red Brocade.png"
      image_8 = Image.open(image_path_8)
      resized_image_8 = image_8.resize((100,100))
      enhan3photo = ImageTk.PhotoImage(resized_image_8)
      enhan3_image.config(image=enhan3photo)
      enhan3_image.image = enhan3photo

      enhan3_name = tk.Label(frame2, text = 'Rich Red Brocade', font=('Arial', 10), wraplength=100)
      enhan3_name.grid(row = 3, column = 3, sticky = 'n')

    if enhancement.get() == "3":
      #'Spectral Husk, Spectral Heart, Spectral Nucleus'
      image_path_6 = f"Materials/enhancement/Spectral Husk.png"
      image_6 = Image.open(image_path_6)
      resized_image_6 = image_6.resize((100,100))
      enhan1photo = ImageTk.PhotoImage(resized_image_6)
      enhan1_image.config(image=enhan1photo)
      enhan1_image.image = enhan1photo

      enhan1_name = tk.Label(frame2, text = 'Spectral Husk', font=('Arial', 10), wraplength=100)
      enhan1_name.grid(row = 3, column = 1, sticky = 'n')

      image_path_7 = f"Materials/enhancement/Spectral Heart.png"
      image_7 = Image.open(image_path_7)
      resized_image_7 = image_7.resize((100,100))
      enhan2photo = ImageTk.PhotoImage(resized_image_7)
      enhan2_image.config(image=enhan2photo)
      enhan2_image.image = enhan2photo

      enhan2_name = tk.Label(frame2, text = 'Spectral Heart', font=('Arial', 10), wraplength=100)
      enhan2_name.grid(row = 3, column = 2, sticky = 'n')

      image_path_8 = f"Materials/enhancement/Spectral Nucleus.png"
      image_8 = Image.open(image_path_8)
      resized_image_8 = image_8.resize((100,100))
      enhan3photo = ImageTk.PhotoImage(resized_image_8)
      enhan3_image.config(image=enhan3photo)
      enhan3_image.image = enhan3photo

      enhan3_name = tk.Label(frame2, text = 'Spectral Nucleus', font=('Arial', 10), wraplength=100)
      enhan3_name.grid(row = 3, column = 3, sticky = 'n')

    if enhancement.get() == "4":
      #'Firm Arrowhead, Sharp Arrowhead, Weathered Arrowhead'
      image_path_6 = f"Materials/enhancement/Firm Arrowhead.png"
      image_6 = Image.open(image_path_6)
      resized_image_6 = image_6.resize((100,100))
      enhan1photo = ImageTk.PhotoImage(resized_image_6)
      enhan1_image.config(image=enhan1photo)
      enhan1_image.image = enhan1photo

      enhan1_name = tk.Label(frame2, text = 'Firm Arrowhead', font=('Arial', 10), wraplength=100)
      enhan1_name.grid(row = 3, column = 1, sticky = 'n')

      image_path_7 = f"Materials/enhancement/Sharp Arrowhead.png"
      image_7 = Image.open(image_path_7)
      resized_image_7 = image_7.resize((100,100))
      enhan2photo = ImageTk.PhotoImage(resized_image_7)
      enhan2_image.config(image=enhan2photo)
      enhan2_image.image = enhan2photo

      enhan2_name = tk.Label(frame2, text = 'Sharp Arrowhead', font=('Arial', 10), wraplength=100)
      enhan2_name.grid(row = 3, column = 2, sticky = 'n')

      image_path_8 = f"Materials/enhancement/Weathered Arrowhead.png"
      image_8 = Image.open(image_path_8)
      resized_image_8 = image_8.resize((100,100))
      enhan3photo = ImageTk.PhotoImage(resized_image_8)
      enhan3_image.config(image=enhan3photo)
      enhan3_image.image = enhan3photo

      enhan3_name = tk.Label(frame2, text = 'Weathered Arrowhead', font=('Arial', 10), wraplength=100)
      enhan3_name.grid(row = 3, column = 3, sticky = 'n')

    if enhancement.get() == "5":
      #'Slime Condensate, Slime Secretions, Slime Concentrate'
      image_path_6 = f"Materials/enhancement/Slime Condensate.png"
      image_6 = Image.open(image_path_6)
      resized_image_6 = image_6.resize((100,100))
      enhan1photo = ImageTk.PhotoImage(resized_image_6)
      enhan1_image.config(image=enhan1photo)
      enhan1_image.image = enhan1photo

      enhan1_name = tk.Label(frame2, text = 'Slime Condensate', font=('Arial', 10), wraplength=100)
      enhan1_name.grid(row = 3, column = 1, sticky = 'n')

      image_path_7 = f"Materials/enhancement/Slime Secretions.png"
      image_7 = Image.open(image_path_7)
      resized_image_7 = image_7.resize((100,100))
      enhan2photo = ImageTk.PhotoImage(resized_image_7)
      enhan2_image.config(image=enhan2photo)
      enhan2_image.image = enhan2photo

      enhan2_name = tk.Label(frame2, text = 'Slime Secretions', font=('Arial', 10), wraplength=100)
      enhan2_name.grid(row = 3, column = 2, sticky = 'n')

      image_path_8 = f"Materials/enhancement/Slime Concentrate.png"
      image_8 = Image.open(image_path_8)
      resized_image_8 = image_8.resize((100,100))
      enhan3photo = ImageTk.PhotoImage(resized_image_8)
      enhan3_image.config(image=enhan3photo)
      enhan3_image.image = enhan3photo

      enhan3_name = tk.Label(frame2, text = 'Slime Concentrate', font=('Arial', 10), wraplength=100)
      enhan3_name.grid(row = 3, column = 3, sticky = 'n')

    if enhancement.get() == "6":
      #'Fungal Spores, Luminescent Pollen, Crystalline Cyst Dust'
      image_path_6 = f"Materials/enhancement/Fungal Spores.png"
      image_6 = Image.open(image_path_6)
      resized_image_6 = image_6.resize((100,100))
      enhan1photo = ImageTk.PhotoImage(resized_image_6)
      enhan1_image.config(image=enhan1photo)
      enhan1_image.image = enhan1photo

      enhan1_name = tk.Label(frame2, text = 'Fungal Spores', font=('Arial', 10), wraplength=100)
      enhan1_name.grid(row = 3, column = 1, sticky = 'n')

      image_path_7 = f"Materials/enhancement/Luminescent Pollen.png"
      image_7 = Image.open(image_path_7)
      resized_image_7 = image_7.resize((100,100))
      enhan2photo = ImageTk.PhotoImage(resized_image_7)
      enhan2_image.config(image=enhan2photo)
      enhan2_image.image = enhan2photo

      enhan2_name = tk.Label(frame2, text = 'Luminescent Pollen', font=('Arial', 10), wraplength=100)
      enhan2_name.grid(row = 3, column = 2, sticky = 'n')

      image_path_8 = f"Materials/enhancement/Crystalline Cyst Dust.png"
      image_8 = Image.open(image_path_8)
      resized_image_8 = image_8.resize((100,100))
      enhan3photo = ImageTk.PhotoImage(resized_image_8)
      enhan3_image.config(image=enhan3photo)
      enhan3_image.image = enhan3photo

      enhan3_name = tk.Label(frame2, text = 'Crystalline Cyst Dust', font=('Arial', 10), wraplength=100)
      enhan3_name.grid(row = 3, column = 3, sticky = 'n')

    if enhancement.get() == "7":
      #'Treasure Hoarder Insignia, Silver Raven Insignia, Golden Raven Insignia'
      image_path_6 = f"Materials/enhancement/Treasure Hoarder Insignia.png"
      image_6 = Image.open(image_path_6)
      resized_image_6 = image_6.resize((100,100))
      enhan1photo = ImageTk.PhotoImage(resized_image_6)
      enhan1_image.config(image=enhan1photo)
      enhan1_image.image = enhan1photo

      enhan1_name = tk.Label(frame2, text = 'Treasure Hoarder Insignia', font=('Arial', 10), wraplength=100)
      enhan1_name.grid(row = 3, column = 1, sticky = 'n')

      image_path_7 = f"Materials/enhancement/Silver Raven Insignia.png"
      image_7 = Image.open(image_path_7)
      resized_image_7 = image_7.resize((100,100))
      enhan2photo = ImageTk.PhotoImage(resized_image_7)
      enhan2_image.config(image=enhan2photo)
      enhan2_image.image = enhan2photo

      enhan2_name = tk.Label(frame2, text = 'Silver Raven Insignia', font=('Arial', 10), wraplength=100)
      enhan2_name.grid(row = 3, column = 2, sticky = 'n')

      image_path_8 = f"Materials/enhancement/Golden Raven Insignia.png"
      image_8 = Image.open(image_path_8)
      resized_image_8 = image_8.resize((100,100))
      enhan3photo = ImageTk.PhotoImage(resized_image_8)
      enhan3_image.config(image=enhan3photo)
      enhan3_image.image = enhan3photo

      enhan3_name = tk.Label(frame2, text = 'Golden Raven Insignia', font=('Arial', 10), wraplength=100)
      enhan3_name.grid(row = 3, column = 3, sticky = 'n')

    if enhancement.get() == "8":
      #'Meshing Gear, Mechanical Spur Gear, Artificed Dynamic Gear'
      image_path_6 = f"Materials/enhancement/Meshing Gear.png"
      image_6 = Image.open(image_path_6)
      resized_image_6 = image_6.resize((100,100))
      enhan1photo = ImageTk.PhotoImage(resized_image_6)
      enhan1_image.config(image=enhan1photo)
      enhan1_image.image = enhan1photo

      enhan1_name = tk.Label(frame2, text = 'Meshing Gear', font=('Arial', 10), wraplength=100)
      enhan1_name.grid(row = 3, column = 1, sticky = 'n')

      image_path_7 = f"Materials/enhancement/Mechanical Spur Gear.png"
      image_7 = Image.open(image_path_7)
      resized_image_7 = image_7.resize((100,100))
      enhan2photo = ImageTk.PhotoImage(resized_image_7)
      enhan2_image.config(image=enhan2photo)
      enhan2_image.image = enhan2photo

      enhan2_name = tk.Label(frame2, text = 'Mechanical Spur Gear', font=('Arial', 10), wraplength=100)
      enhan2_name.grid(row = 3, column = 2, sticky = 'n')

      image_path_8 = f"Materials/enhancement/Artificed Dynamic Gear.png"
      image_8 = Image.open(image_path_8)
      resized_image_8 = image_8.resize((100,100))
      enhan3photo = ImageTk.PhotoImage(resized_image_8)
      enhan3_image.config(image=enhan3photo)
      enhan3_image.image = enhan3photo

      enhan3_name = tk.Label(frame2, text = 'Artificed Dynamic Gear', font=('Arial', 10), wraplength=100)
      enhan3_name.grid(row = 3, column = 3, sticky = 'n')

    if enhancement.get() == "9":
      #'Damaged Mask, Stained Mask, Ominous Mask'
      image_path_6 = f"Materials/enhancement/Damaged Mask.png"
      image_6 = Image.open(image_path_6)
      resized_image_6 = image_6.resize((100,100))
      enhan1photo = ImageTk.PhotoImage(resized_image_6)
      enhan1_image.config(image=enhan1photo)
      enhan1_image.image = enhan1photo

      enhan1_name = tk.Label(frame2, text = 'Damaged Mask', font=('Arial', 10), wraplength=100)
      enhan1_name.grid(row = 3, column = 1, sticky = 'n')

      image_path_7 = f"Materials/enhancement/Stained Mask.png"
      image_7 = Image.open(image_path_7)
      resized_image_7 = image_7.resize((100,100))
      enhan2photo = ImageTk.PhotoImage(resized_image_7)
      enhan2_image.config(image=enhan2photo)
      enhan2_image.image = enhan2photo

      enhan2_name = tk.Label(frame2, text = 'Stained Mask', font=('Arial', 10), wraplength=100)
      enhan2_name.grid(row = 3, column = 2, sticky = 'n')

      image_path_8 = f"Materials/enhancement/Ominous Mask.png"
      image_8 = Image.open(image_path_8)
      resized_image_8 = image_8.resize((100,100))
      enhan3photo = ImageTk.PhotoImage(resized_image_8)
      enhan3_image.config(image=enhan3photo)
      enhan3_image.image = enhan3photo

      enhan3_name = tk.Label(frame2, text = 'Ominous Mask', font=('Arial', 10), wraplength=100)
      enhan3_name.grid(row = 3, column = 3, sticky = 'n')

    if enhancement.get() == "10":
      #'Recruit's Insignia, Sergeant's Insignia, Lieutenant's Insignia'
      image_path_6 = f"Materials/enhancement/Recruit's Insignia.png"
      image_6 = Image.open(image_path_6)
      resized_image_6 = image_6.resize((100,100))
      enhan1photo = ImageTk.PhotoImage(resized_image_6)
      enhan1_image.config(image=enhan1photo)
      enhan1_image.image = enhan1photo

      enhan1_name = tk.Label(frame2, text = "Recruit's Insignia", font=('Arial', 10), wraplength=100)
      enhan1_name.grid(row = 3, column = 1, sticky = 'n')

      image_path_7 = f"Materials/enhancement/Sergeant's Insignia.png"
      image_7 = Image.open(image_path_7)
      resized_image_7 = image_7.resize((100,100))
      enhan2photo = ImageTk.PhotoImage(resized_image_7)
      enhan2_image.config(image=enhan2photo)
      enhan2_image.image = enhan2photo

      enhan2_name = tk.Label(frame2, text = "Sergeant's Insignia", font=('Arial', 10), wraplength=100)
      enhan2_name.grid(row = 3, column = 2, sticky = 'n')

      image_path_8 = f"Materials/enhancement/Lieutenant's Insignia.png"
      image_8 = Image.open(image_path_8)
      resized_image_8 = image_8.resize((100,100))
      enhan3photo = ImageTk.PhotoImage(resized_image_8)
      enhan3_image.config(image=enhan3photo)
      enhan3_image.image = enhan3photo

      enhan3_name = tk.Label(frame2, text = "Lieutenant's Insignia", font=('Arial', 10), wraplength=100)
      enhan3_name.grid(row = 3, column = 3, sticky = 'n')
      
    if enhancement.get() == "11":
      #'Transoceanic Pearl, Transoceanic Chunk, Xenochromatic Crystal'
      image_path_6 = f"Materials/enhancement/Transoceanic Pearl.png"
      image_6 = Image.open(image_path_6)
      resized_image_6 = image_6.resize((100,100))
      enhan1photo = ImageTk.PhotoImage(resized_image_6)
      enhan1_image.config(image=enhan1photo)
      enhan1_image.image = enhan1photo

      enhan1_name = tk.Label(frame2, text = 'Transoceanic Pearl', font=('Arial', 10), wraplength=100)
      enhan1_name.grid(row = 3, column = 1, sticky = 'n')

      image_path_7 = f"Materials/enhancement/Transoceanic Chunk.png"
      image_7 = Image.open(image_path_7)
      resized_image_7 = image_7.resize((100,100))
      enhan2photo = ImageTk.PhotoImage(resized_image_7)
      enhan2_image.config(image=enhan2photo)
      enhan2_image.image = enhan2photo

      enhan2_name = tk.Label(frame2, text = 'Transoceanic Chunk', font=('Arial', 10), wraplength=100)
      enhan2_name.grid(row = 3, column = 2, sticky = 'n')

      image_path_8 = f"Materials/enhancement/Xenochromatic Crystal.png"
      image_8 = Image.open(image_path_8)
      resized_image_8 = image_8.resize((100,100))
      enhan3photo = ImageTk.PhotoImage(resized_image_8)
      enhan3_image.config(image=enhan3photo)
      enhan3_image.image = enhan3photo

      enhan3_name = tk.Label(frame2, text = 'Xenochromatic Crystal', font=('Arial', 10), wraplength=100)
      enhan3_name.grid(row = 3, column = 3, sticky = 'n')

    if enhancement.get() == "12":
      #'Whopperflower Nectar, Shimmering Nectar, Energy Nectar'
      image_path_6 = f"Materials/enhancement/Whopperflower Nectar.png"
      image_6 = Image.open(image_path_6)
      resized_image_6 = image_6.resize((100,100))
      enhan1photo = ImageTk.PhotoImage(resized_image_6)
      enhan1_image.config(image=enhan1photo)
      enhan1_image.image = enhan1photo

      enhan1_name = tk.Label(frame2, text = 'Whopperflower Nectar', font=('Arial', 10), wraplength=100)
      enhan1_name.grid(row = 3, column = 1, sticky = 'n')

      image_path_7 = f"Materials/enhancement/Shimmering Nectar.png"
      image_7 = Image.open(image_path_7)
      resized_image_7 = image_7.resize((100,100))
      enhan2photo = ImageTk.PhotoImage(resized_image_7)
      enhan2_image.config(image=enhan2photo)
      enhan2_image.image = enhan2photo

      enhan2_name = tk.Label(frame2, text = 'Shimmering Nectar', font=('Arial', 10), wraplength=100)
      enhan2_name.grid(row = 3, column = 2, sticky = 'n')

      image_path_8 = f"Materials/enhancement/Energy Nectar.png"
      image_8 = Image.open(image_path_8)
      resized_image_8 = image_8.resize((100,100))
      enhan3photo = ImageTk.PhotoImage(resized_image_8)
      enhan3_image.config(image=enhan3photo)
      enhan3_image.image = enhan3photo

      enhan3_name = tk.Label(frame2, text = 'Energy Nectar', font=('Arial', 10), wraplength=100)
      enhan3_name.grid(row = 3, column = 3, sticky = 'n')

    if enhancement.get() == "13":
      #'Old Handguard, Kageuchi Handguard, Famed Handguard'
      image_path_6 = f"Materials/enhancement/Old Handguard.png"
      image_6 = Image.open(image_path_6)
      resized_image_6 = image_6.resize((100,100))
      enhan1photo = ImageTk.PhotoImage(resized_image_6)
      enhan1_image.config(image=enhan1photo)
      enhan1_image.image = enhan1photo

      enhan1_name = tk.Label(frame2, text = 'Old Handguard', font=('Arial', 10), wraplength=100)
      enhan1_name.grid(row = 3, column = 1, sticky = 'n')

      image_path_7 = f"Materials/enhancement/Kageuchi Handguard.png"
      image_7 = Image.open(image_path_7)
      resized_image_7 = image_7.resize((100,100))
      enhan2photo = ImageTk.PhotoImage(resized_image_7)
      enhan2_image.config(image=enhan2photo)
      enhan2_image.image = enhan2photo

      enhan2_name = tk.Label(frame2, text = 'Kageuchi Handguard', font=('Arial', 10), wraplength=100)
      enhan2_name.grid(row = 3, column = 2, sticky = 'n')

      image_path_8 = f"Materials/enhancement/Famed Handguard.png"
      image_8 = Image.open(image_path_8)
      resized_image_8 = image_8.resize((100,100))
      enhan3photo = ImageTk.PhotoImage(resized_image_8)
      enhan3_image.config(image=enhan3photo)
      enhan3_image.image = enhan3photo

      enhan3_name = tk.Label(frame2, text = 'Famed Handguard', font=('Arial', 10), wraplength=100)
      enhan3_name.grid(row = 3, column = 3, sticky = 'n')

    image_path_9 = f"Materials/flower/{flower.get()}.png"
    image_9 = Image.open(image_path_9)
    resized_image_9 = image_9.resize((100,100))
    flophoto = ImageTk.PhotoImage(resized_image_9)
    flower_image.config(image=flophoto)
    flower_image.image = flophoto

    flower_name = tk.Label(frame2, text = f'{flower.get()}', font=('Arial', 10), wraplength=100)
    flower_name.grid(row = 3, column = 4, sticky = 'n')

    image_path_10 = f"Materials/normal boss/{normal_boss.get()}.png"
    image_10= Image.open(image_path_10)
    resized_image_10 = image_10.resize((100,100))
    norphoto = ImageTk.PhotoImage(resized_image_10)
    normal_boss_image.config(image=norphoto)
    normal_boss_image.image = norphoto
    
    normal_material = tk.Label(frame2, text = normal_boss.get(), font=('Arial', 10), wraplength=100)
    normal_material.grid(row = 3, column = 5, sticky = 'n')

  else:
    pass

#character calculator features
root = tk.Tk()
root.geometry("1300x900")
root.title("Character Level Calculator")

#grid
root.columnconfigure((0,1,2), weight = 1)
root.rowconfigure((0,1), weight = 1)
root.rowconfigure(2, weight = 10)

#labels
title = tk.Label(root, text = "Select character to show their Materials.", font = ('Arial', 22))
title.grid(row = 0, column = 0, columnspan = 2, sticky = 'w', padx = 20, pady = 10)

search = tk.Label(root, text = "Select Character ", font = ('Arial', 20))
search.grid(row = 1, column = 0, sticky = 'e', pady = (0,6))

#add frame1
frame1 = ttk.LabelFrame(root, height = 750, width = 1200)
frame1.grid_propagate(False)
frame1.grid(row = 2, columnspan=3, column = 0)

frame1_width = frame1.winfo_width()
frame1_height = frame1.winfo_height()

#add frame2
frame2 = ttk.LabelFrame(frame1, height = 600, width = 900)
frame2.place(x = frame1_width + 580, y = frame1_height + 400, anchor = "center")

# Add widgets to the new window/frame
character_info_label = tk.Label(frame1, text="Character's Materials", font=('Arial', 20))
character_info_label.place(x = frame1_width + 580, y = frame1_height + 25, anchor = "center")

#search box
global CharaChosen
boxvalue = tk.StringVar()
CharaChosen = ttk.Combobox(root, textvariable=boxvalue, values=namelist, width=42)
CharaChosen.grid(row = 1, column = 1 , sticky = 'w', padx = (0,20))

global normal_boss, ascension, enhancement, flower
normal_boss = tk.StringVar()
normal_boss.set('')
ascension = tk.StringVar()
ascension.set('')
enhancement = tk.StringVar()
enhancement.set('')
flower = tk.StringVar()
flower.set('')

AddCharacterButton = ttk.Button(root, text="SEARCH", width = 8,command = frame)
AddCharacterButton.grid(row = 1, column = 1, sticky = 'e', padx = (0,150))

CharaChosen.current()
CharaChosen.bind('<KeyRelease>', Search)

root.mainloop()