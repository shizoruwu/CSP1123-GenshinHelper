import datetime, time
import win11toast
import pystray
import sqlite3
import multiprocessing
import PIL.Image
import os

current_path = os.path.abspath(os.getcwd())

def fetch(type="notification list"):
    DBconnection = sqlite3.connect("genshindata.db")
    DBcursor = DBconnection.cursor()

    if type == "daily notification":
        daily_notification_status = DBcursor.execute("SELECT Status FROM notification WHERE Notification = 'DAILY_NOTIFICATION'")
        daily_notification_status = daily_notification_status.fetchall()
        return daily_notification_status[0][0]

    elif type == "advanced notification":
        advanced_notification_status = DBcursor.execute("SELECT Status FROM notification WHERE Notification = 'ADVANCED_NOTIFICATION'")
        advanced_notification_status = advanced_notification_status.fetchall()
        return advanced_notification_status[0][0]
    
    elif type == "notice time":
        get_time = DBcursor.execute("SELECT Status FROM notification WHERE Notification = 'DAILY_NOTIFICATION_TIME'")
        get_time = get_time.fetchall()
        return get_time[0][0]

    elif type == "notification list":
        notification = DBcursor.execute("SELECT Notification FROM notification WHERE Status = '1' AND rowid > 5 AND rowid < 13")
        notification = notification.fetchall()
        notification_list = []
        for i in range(len(notification)):
            notification_list.append(notification[i][0]) 
        return notification_list
    
    elif type == "resin":
        resin_reset = DBcursor.execute("SELECT Status FROM notification WHERE Notification = 'RESIN_RESET'")
        resin_reset = resin_reset.fetchall()
        # resin_time = []
        # resin_time.append(resin_reset[0])
        resin_time = resin_reset[0][0]
        resin_time = resin_time.split(sep=":")
        return resin_time[0], resin_time[1]
        

    # Get Todo amount
    elif type == "todo":
        data = DBcursor.execute("SELECT * FROM tasks") # Read
        data = data.fetchall() # Get
        print(data)
        amount = 0
        character = []
        weapon = []
        for i in range(len(data)):
            if data[i][1] == 'False':
                amount += 1
        for i in range(len(data)):
            if "Upgrade" in data[i][0] and data[i][1] == 'False':
                temp = data[i][0]
                if "Level" in temp:
                    character.append(temp.split(sep=" ")[1])
                else:
                    temp = temp.split(sep=" ")[1:][0:]
                    temp2 = ""
                    for i in range(len(temp)):
                        if i == len(temp) - 1:
                            temp2 += temp[i]
                        else:
                            temp2 += temp[i]+" "
                    weapon.append(temp2)
        return amount, character, weapon

def click(a):
    import GenshinHelper_Main

def toaster(type):
    msg = ""
    characters = ""
    weapons = ""
    todo_amount, chr, wp = fetch("todo")
    for i in chr:
        characters += i + ", "
    for i in wp:
        weapons += i + ", "
        
    # weapons = "Kagura's Verity"

    # Daily notification messages
    checkin = "Hi! It's the time to check-in!\n"
    todo = f"You have {todo_amount} To-Do Tasks left. "
    character = f"You planned to upgrade:\n- Character(s): {characters}\n- Weapon(s): {weapons}"
    # Avanced notification messages
    resin = "You resin is about to overflow!!"
    boss = "Weekly bosses has been reset today."
    abyss = "Abyss bosses has been reset today."
    paimon = "Paimon's Shop has been reset today."
    
    resin_toast_allow = False
    for notification in fetch():
        match notification:
            case "Daily Check-in":
                print("yes")
                msg += checkin
            case "To-Do Tasks":
                print("yes")
                msg += todo
            case "Characters/Weapons planned to be upgraded":
                msg += character
            case "Resin Overflow Reminder":
                resin_toast_allow = True
            case "Abyss Reset":
                abyss_toasted = False
            case "Weekly Bosses Reset":
                boss_toasted = False
            case "Paimon's Shop Reset":
                paimon_toasted = False

    buttons=[
                {'activationType': 'protocol', 'arguments': 'http:', 'content': 'View Details'},
                {'activationType': 'protocol', 'arguments': 'https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id=e202102251931481', 'content': 'Web Check-in'}
            ]
    
    if type == 'normal':
        win11toast.toast('Genhsin Helper', msg, buttons=buttons, on_click = click, duration = "10")
    elif type == 'game':
        win11toast.toast('Genhsin Helper', msg, button='View Details', on_click = click, duration = "10")

    elif type == 'resin' and resin_toast_allow == True:
        win11toast.toast('Genhsin Helper', resin, button='View Details', on_click = click, duration = "10")
        resin_toasted = True
    elif type == 'boss' and boss_toasted == False:
        win11toast.toast('Genhsin Helper', boss, button='View Details', on_click = click, duration = "10")
    elif type == 'abyss' and abyss_toasted == False:
        win11toast.toast('Genhsin Helper', abyss, button='View Details', on_click = click, duration = "10")
    elif type == 'paimon' and paimon_toasted == False:
        win11toast.toast('Genhsin Helper', paimon, button='View Details', on_click = click, duration = "10")

def start_service():
    # Add a zero get a proper 24 Hrs Format
    hour = fetch("notice time")
    if int(hour) >= 0 and int(hour) < 10:
        hour = "0" + hour[0][0]

    global normal_toasted
    global resin_toasted
    global boss_toasted
    global abyss_toasted
    global paimon_toasted

    # Restriction
    normal_toasted = False
    resin_toasted = False

    boss_toasted = True
    abyss_toasted = True
    paimon_toasted = True

    while True:
        current_time = datetime.datetime.now().strftime("%H")
        # current_time = "12"
        current_min = datetime.datetime.now().strftime("%M")
        current_weekday = datetime.datetime.now().strftime("%a")
        today_date = datetime.datetime.now().strftime("%d")
        time.sleep(1)

        ## Reset restriction
        if fetch("daily notification") == "0":
            normal_toasted = True
        else:
            if hour != hour:
                normal_toasted = False

        if fetch("advanced notification") == "0":
            resin_toasted = True
            boss_toasted = True
            abyss_toasted = True
            paimon_toasted = True
        else:
            if current_min != fetch("resin")[1]:
                resin_toasted = False
            elif current_weekday == "Tue":
                boss_toasted = True
            elif today_date == "02" or today_date == "17":
                abyss_toasted = True
                paimon_toasted = True

        # Daily notification
        if current_time == hour and normal_toasted == False:
            toaster('normal')
            normal_toasted = True
        # Resin
        elif current_time == fetch("resin")[0] and current_min == fetch("resin")[1] and resin_toasted == False:
            toaster("resin")
            resin_toasted = True
        # Every Monday 4am reset weekly bosses
        elif current_weekday == "Mon" and current_time == "04":
            toaster('boss')
        # Every month 1st and 16 reset Abyss
        elif today_date == "01" or today_date == "16":
            toaster("abyss")
        # Every month 1st Paimon's shop reset
        elif today_date == "01":
            toaster("paimon")
      
def notifier():
    # fetch("todo")
    start_service()

    
## Tray stuffs
def quit(pid):
    tray.stop()
    os.popen(f'taskkill /pid {pid} /f')
    DBconnection = sqlite3.connect("genshindata.db")
    DBcursor = DBconnection.cursor()
    DBcursor.execute(f"UPDATE notification SET Status = '0' WHERE Notification = 'DAILY_NOTIFICATION'")
    DBcursor.execute(f"UPDATE notification SET Status = '0' WHERE Notification = 'ADVANCED_NOTIFICATION'")
    DBconnection.commit()
    DBconnection.close()

def sys_tray(pid):
    global tray
    
    image = PIL.Image.open(current_path + r"\Assets\Image\Paimon_tray.png")
    # resized_image= image.resize((1000,1000))
    tray = pystray.Icon("Tray", image, title="Genshin Helper Notification", menu=pystray.Menu(
        pystray.MenuItem("Exit", lambda:quit(pid=pid)),
        pystray.MenuItem("Open", click)
    ))
    # Get tray PID
    pid_tray = os.getpid()
    DBconnection = sqlite3.connect("genshindata.db")
    DBcursor = DBconnection.cursor()
    DBcursor.execute(f"UPDATE notification SET Status = {pid_tray} WHERE Notification = 'PID_TRAY'")
    DBconnection.commit()
    DBconnection.close()
    tray.run()

def main():
    # Get PID
    pid_notifier = os.getpid()
    DBconnection = sqlite3.connect("genshindata.db")
    DBcursor = DBconnection.cursor()
    DBcursor.execute(f"UPDATE notification SET Status = {pid_notifier} WHERE Notification = 'PID_NOTIFIER'")
    DBconnection.commit()
    DBconnection.close()
    # Start
    tray_process = multiprocessing.Process(target=sys_tray, args=([pid_notifier])) 
    tray_process.start()
    notifier()

if __name__ == "__main__":
    main()
    

