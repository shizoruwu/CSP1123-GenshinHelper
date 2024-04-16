#This is a Project of TT4L-06 CSP1123

import tkinter as tk 
import csv

###Main Menu

###Character Database
CharacterNames = ['Albedo',]


#Character Quality
Character_5stars = ['Albedo',]
Character_4stars = []

#Character Search Features
def search():
    Character = input('Insert Character')
    if Character in Character_5stars:
        return '5 Star'
    

