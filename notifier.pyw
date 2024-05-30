
import time
# from win11toast import toast
import win11toast
import os
import sqlite3
# 1st and 16th of the month is the reset.

def fetch_todo():
    DBconnection = sqlite3.connect("genshindata.db")
    DBcursor = DBconnection.cursor()

    data = DBcursor.execute("SELECT * FROM tasks") # Read
    data = data.fetchall() # Get
    amount = 0
    for i in range(len(data)):
        if data[i][1] == 'False':
            amount += 1

    DBconnection.close()
    return amount

def toast(type):
    characters = 'KeQing, Nahida'
    weapons = "Kagura's Verity"
    checkin = "Hi! It's the time to check-in!\n"
    todo = f"You have {fetch_todo()} To-Do Tasks left. "
    character = f"You planned to upgrade:\n- Characters: {characters}\n"
    weapon = f"- Weapon: {weapons}"
    resin = "You resin is about to overflow!!"
    boss = "Weekly bosses has been reset today!!"
    abyss = "Abyss bosses has been reset today."


    buttons=[
                {'activationType': 'protocol', 'arguments': 'http:', 'content': 'View Details'},
                {'activationType': 'protocol', 'arguments': 'https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id=e202102251931481', 'content': 'Web Check-in'}
            ]
    
    if type == 'normal':
        win11toast.toast('Genhsin Helper', checkin+todo+character+weapon, buttons=buttons, on_click = click, duration = 10)
    elif type == 'game':
        win11toast.toast('Genhsin Helper', todo+character+weapon, button=['View Details'], on_click = click, duration = 10)
    elif type == 'resin':
        win11toast.toast('Genhsin Helper', resin, buttons=buttons, on_click = click, duration = 10)
    elif type == 'boss':
        win11toast.toast('Genhsin Helper', boss, buttons=buttons, on_click = click, duration = 10)
    elif type == 'abyss':
        win11toast.toast('Genhsin Helper', abyss, buttons=buttons, on_click = click, duration = 10)

def click(a):
    import test_main

def start_service(hour):
    while True:
        # current_time = time.strftime("%H:%M:%S")
        current_time = time.strftime("%S")
        # current_time = time.strftime("%H")
        # os.system("cls")
        # print(current_time)
        time.sleep(1)

        
        if current_time == hour:
            toast('normal')
            # time.sleep(3600) # 1h-3600s 1m-360s
            time.sleep(5) # 1h-3600s 1m-360s

        



start_service('50')
        
# start_service("30", "Hi! It's the time to check-in!\n"
#               "You have 4 To-Do Tasks left. "
#               "You planned to upgrade:\n"
#               "- Characters: Albedo, Nahida\n"
#               "- Weapon: A, B")


# def startup(isStartup):
#     if isStartup:
#         os.system('schtasks /change /tn "Genshin Helper Notification" /ENABLE')
#     elif isStartup == False:
#         os.system('schtasks /change /tn "Genshin Helper Notification" /DISABLE')