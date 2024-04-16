#This is a Project of TT4L-06 CSP1123

import tkinter as tk 
import csv

###Main Menu

###Character Database
CharacterNames = ['Albedo',]

#Character Quality
Character_5stars = ['Albedo',]
Character_4stars = 

#Character Search Features
rows = []

with open('Character.csv','r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        rows.append(row)

print(header)
print(rows)