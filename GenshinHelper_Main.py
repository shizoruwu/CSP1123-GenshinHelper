# Top - Side / Bar

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ctypes import windll
from PIL import Image, ImageTk
import os

import todo
import weapon_search
import character_search
import character_level
import resin_timer
import notifier_gui

windll.shcore.SetProcessDpiAwareness(1)
root = ttk.Window(themename="light_4")
root.title("Genshin Helper")
root.geometry("1500x900")

s = ttk.Style()
s.configure('green.TButton', foreground = "green")
s.configure('bd.TButton', borderwidth=5)
s.configure('font.TLabel', font=("Georgia", 15))
s.configure('fontt.TLabel', font=("Georgia", 15))
s.configure('grey.TFrame', background="grey")

topFrame = ttk.LabelFrame(root)
topFrame.grid(column=1, row=1, sticky=W, padx=10, columnspan=2)
title = ttk.Label(topFrame, text=" Genshin Helper", style="font.TLabel", bootstyle="primary")
sideBarFrame = ttk.Frame(root)
sideBarFrame.grid(column=1, row=2, sticky=NW, pady=5, ipady=500, ipadx=5)

root.update()
sideBarFrame.update()


## Features
characterSearch = character_search.charsearch(root)
characterSearch.grid(column=2, row=2, padx=10, pady=15, sticky=NW)

CharacterLevelCalc = character_level.characterlevel(root)
CharacterLevelCalc.grid(column=2, row=2, padx=10, pady=15, sticky=NW, ipadx=48, ipady=5)
CharacterLevelCalc.grid_remove()

weapon = weapon_search.weaponsearch(root)
weapon.grid(column=2, row=2,padx=10, pady=15, sticky=NW)
weapon.grid_remove()

resin_timer = resin_timer.resintimer(root)
resin_timer.grid(column=2, row=2, padx=10, pady=15, sticky=NW, ipadx=301, ipady=60)
resin_timer.grid_remove()

todoList = todo.ToDoAppFrame(root)
todoList.grid(column=2, row=2, padx=10, pady=15, sticky=NW)
todoList.grid_remove()

notifier = notifier_gui.NotificationFrame(root)
notifier.grid(column=2, row=2, padx=10, pady=15, sticky=NW, ipadx=1500, ipady=100)
notifier.grid_remove()

## Side bar functions
def CharacterSearch_grid():
    characterSearch.grid()
    CharacterLevelCalc.grid_remove()
    weapon.grid_remove()
    resin_timer.grid_remove()
    todoList.grid_remove()
    notifier.grid_remove()
    
    characterSearch_button.config(bootstyle='danger', image=characterIconW)
    characterLevelCalc_button.config(bootstyle='primary-outline', image=calcIconB)
    weapon_button.config(bootstyle='primary-outline', image=weaponsIconB)
    resin_button.config(bootstyle='primary-outline')
    todo_button.config(bootstyle='primary-outline', image=todoIconB)
    notifier_button.config(bootstyle='primary-outline', image=notificationIconB)

def CharacterLevelCalc_grid():
    characterSearch.grid_remove()
    CharacterLevelCalc.grid()
    weapon.grid_remove()
    resin_timer.grid_remove()
    todoList.grid_remove()
    notifier.grid_remove()

    characterSearch_button.config(bootstyle='primary-outline', image=characterIconB)
    characterLevelCalc_button.config(bootstyle='danger', image=calcIconW)
    weapon_button.config(bootstyle='primary-outline', image=weaponsIconB)
    resin_button.config(bootstyle='primary-outline')
    todo_button.config(bootstyle='primary-outline', image=todoIconB)
    notifier_button.config(bootstyle='primary-outline', image=notificationIconB)

def weapon_grid():
    characterSearch.grid_remove()
    CharacterLevelCalc.grid_remove()
    weapon.grid()
    resin_timer.grid_remove()
    todoList.grid_remove()
    notifier.grid_remove()

    characterSearch_button.config(bootstyle='primary-outline', image=characterIconB)
    characterLevelCalc_button.config(bootstyle='primary-outline', image=calcIconB)
    weapon_button.config(bootstyle='danger', image=weaponsIconW)
    resin_button.config(bootstyle='primary-outline')
    todo_button.config(bootstyle='primary-outline', image=todoIconB)
    notifier_button.config(bootstyle='primary-outline', image=notificationIconB)

def resin_timer_grid():
    characterSearch.grid_remove()
    CharacterLevelCalc.grid_remove()
    weapon.grid_remove()
    resin_timer.grid()
    todoList.grid_remove()
    notifier.grid_remove()

    characterSearch_button.config(bootstyle='primary-outline', image=characterIconB)
    characterLevelCalc_button.config(bootstyle='primary-outline', image=calcIconB)
    weapon_button.config(bootstyle='primary-outline', image=weaponsIconB)
    resin_button.config(bootstyle='danger')
    todo_button.config(bootstyle='primary-outline', image=todoIconB)
    notifier_button.config(bootstyle='primary-outline', image=notificationIconB)

def todo_grid():
    characterSearch.grid_remove()
    CharacterLevelCalc.grid_remove()
    weapon.grid_remove()
    resin_timer.grid_remove()
    todoList.grid()
    notifier.grid_remove()

    characterSearch_button.config(bootstyle='primary-outline', image=characterIconB)
    characterLevelCalc_button.config(bootstyle='primary-outline', image=calcIconB)
    weapon_button.config(bootstyle='primary-outline', image=weaponsIconB)
    resin_button.config(bootstyle='primary-outline')
    todo_button.config(bootstyle='danger', image=todoIconW)
    notifier_button.config(bootstyle='primary-outline', image=notificationIconB)

def notifier_grid():
    characterSearch.grid_remove()
    CharacterLevelCalc.grid_remove()
    weapon.grid_remove()
    resin_timer.grid_remove()
    todoList.grid_remove()
    notifier.grid()

    characterSearch_button.config(bootstyle='primary-outline', image=characterIconB)
    characterLevelCalc_button.config(bootstyle='primary-outline', image=calcIconB)
    weapon_button.config(bootstyle='primary-outline', image=weaponsIconB)
    resin_button.config(bootstyle='primary-outline')
    todo_button.config(bootstyle='primary-outline', image=todoIconB)
    notifier_button.config(bootstyle='danger', image=notificationIconW)



## Icon 
current_path = os.path.abspath(os.getcwd())
characterImgB = Image.open(current_path + "\Image\Character_icon_black.png")
characterIconB = ImageTk.PhotoImage(characterImgB)
characterImgW = Image.open(current_path + "\Image\Character_icon_white.png")
characterIconW = ImageTk.PhotoImage(characterImgW)
calcImgB = Image.open(current_path + "\Image\Calc_icon_black.png")
calcIconB = ImageTk.PhotoImage(calcImgB)
calcImgW = Image.open(current_path + "\Image\Calc_icon_white.png")
calcIconW = ImageTk.PhotoImage(calcImgW)
weaponsImgB = Image.open(current_path + "\Image\Weapons_icon_black.png")
weaponsIconB = ImageTk.PhotoImage(weaponsImgB)
weaponsImgW = Image.open(current_path + "\Image\Weapons_icon_white.png")
weaponsIconW = ImageTk.PhotoImage(weaponsImgW)
resinImg = Image.open(current_path + "\Image\\resin.png")
resinIcon = ImageTk.PhotoImage(resinImg)
todoImgB = Image.open(current_path + "\Image\Todo_icon_black.png")
todoIconB = ImageTk.PhotoImage(todoImgB)
todoImgW = Image.open(current_path + "\Image\Todo_icon_white.png")
todoIconW = ImageTk.PhotoImage(todoImgW)
notificationImgB = Image.open(current_path + "\Image\\notification_icon_black.png")
notificationIconB = ImageTk.PhotoImage(notificationImgB)
notificationImgW = Image.open(current_path + "\Image\\notification_icon_white.png")
notificationIconW = ImageTk.PhotoImage(notificationImgW)

## Side bar
characterSearch_button = ttk.Button(sideBarFrame, text="Chacracters", image=characterIconW, compound=LEFT, width=10, padding=10, command=CharacterSearch_grid, bootstyle='danger', takefocus=False)
characterSearch_button.grid(column=1, row=1, padx=10, pady=15)
characterLevelCalc_button = ttk.Button(sideBarFrame, text="Character\nCalculator", image=calcIconB, compound=LEFT, width=10, padding=10, command=CharacterLevelCalc_grid, bootstyle='primary-outline', takefocus=False)
characterLevelCalc_button.grid(column=1, row=2, padx=10, pady=(0, 15))
weapon_button = ttk.Button(sideBarFrame, text="Weapons", image=weaponsIconB, compound=LEFT, width=10, padding=10, command=weapon_grid, bootstyle='primary-outline', takefocus=False)
weapon_button.grid(column=1, row=3, padx=10, pady=(0, 15))
resin_button = ttk.Button(sideBarFrame, text="Resin Timer", image=resinIcon, compound=LEFT, width=10, padding=10, command=resin_timer_grid, bootstyle='primary-outline', takefocus=False)
resin_button.grid(column=1, row=4, padx=10, pady=(0, 15))
todo_button = ttk.Button(sideBarFrame, text="To-Do List", image=todoIconB, compound=LEFT, width=10, padding=10, command=todo_grid, bootstyle='primary-outline', takefocus=False)
todo_button.grid(column=1, row=5, padx=10, pady=(0, 15))
notifier_button = ttk.Button(sideBarFrame, text="Notification", image=notificationIconB, compound=LEFT, width=10, padding=10, command=notifier_grid, bootstyle='primary-outline', takefocus=False)
notifier_button.grid(column=1, row=6, padx=10, pady=(0, 15))
# ttk.Button(sideBarFrame, width=15, padding=13, bootstyle='primary', takefocus=False).grid(column=0, row=4, sticky=W, ipady=200)

sideBarFrame.update()
title.grid(column=1, row=1, sticky=W, pady=(0, 10), padx=(5, root.winfo_width() - (sideBarFrame.winfo_width() + 50) ))

root.mainloop()