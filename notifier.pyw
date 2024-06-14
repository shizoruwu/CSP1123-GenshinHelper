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
        notification = DBcursor.execute("SELECT Notification FROM notification WHERE Status = '1' AND rowid > 5")
        notification = notification.fetchall()
        notification_list = []
        for i in range(len(notification)):
            notification_list.append(notification[i][0]) 
        return notification_list

    # Get Todo amount
    elif type == "todo":
        data = DBcursor.execute("SELECT * FROM tasks") # Read
        data = data.fetchall() # Get
        print(data)
        amount = 0
        character = []
        for i in range(len(data)):
            if data[i][1] == 'False':
                amount += 1
        for i in range(len(data)):
            if "Upgrade" in data[i][0] and data[i][1] == 'False':
                temp = data[i][0]
                character.append(temp.split(sep=" ")[1])
        return amount, character

def click(a):
    import GenshinHelper_Main

def toaster(type):
    msg = ""
    characters = ""
    todo_amount, chr = fetch("todo")
    for i in chr:
        characters += i + ", "
        
    # weapons = "Kagura's Verity"

    # Daily notification messages
    checkin = "Hi! It's the time to check-in!\n"
    todo = f"You have {todo_amount} To-Do Tasks left. "
    character = f"You planned to upgrade:\n- Characters: {characters}\n"
    # Avanced notification messages
    resin = "You resin is about to overflow!!"
    boss = "Weekly bosses has been reset today."
    abyss = "Abyss bosses has been reset today."
    paimon = "Paimon's Shop has been reset today."
    

    for notification in fetch():
        match notification:
            case "Daily Check-in":
                print("yes")
                msg += checkin
            case "To-Do Tasks":
                print("yes")
                msg += todo
            case "Characters planned to be upgraded":
                msg += character
            case "Resin Overflow Reminder":
                print("yes")
            case "Abyss Reset":
                print("yes")
            case "Weekly Bosses Reset":
                print("yes")
            case "Paimon's Shop Reset":
                print("yes")

    buttons=[
                {'activationType': 'protocol', 'arguments': 'http:', 'content': 'View Details'},
                {'activationType': 'protocol', 'arguments': 'https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id=e202102251931481', 'content': 'Web Check-in'}
            ]
    
    if type == 'normal':
        win11toast.toast('Genhsin Helper', msg, buttons=buttons, on_click = click, duration = "10")
    elif type == 'game':
        win11toast.toast('Genhsin Helper', msg, button='View Details', on_click = click, duration = "10")

    elif type == 'resin':
        win11toast.toast('Genhsin Helper', resin, button='View Details', on_click = click, duration = "10")
    elif type == 'boss':
        win11toast.toast('Genhsin Helper', boss, button='View Details', on_click = click, duration = "10")
    elif type == 'abyss':
        win11toast.toast('Genhsin Helper', abyss, button='View Details', on_click = click, duration = "10")
    elif type == 'paimon':
        win11toast.toast('Genhsin Helper', paimon, button='View Details', on_click = click, duration = "10")

def start_service():
    # Add a zero get a proper 24 Hrs Format
    hour = fetch("notice time")
    hour = hour[0][0]
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
    boss_toasted = False
    abyss_toasted = False
    paimon_toasted = False

    daily_notification_state = fetch("daily notification")
    advanced_notification_state = fetch("advanced notification")

    while True:
        current_time = datetime.datetime.now().strftime("%H")
        # current_time = "00"
        current_weekday = datetime.datetime.now().strftime("%a")
        today_date = datetime.datetime.now().strftime("%d")

        time.sleep(1)
        # Daily notification
        if current_time == hour and normal_toasted == False:
            toaster('normal')
            normal_toasted = True
        # Every Monday 4am reset weekly bosses
        elif current_weekday == "Mon" and current_time == "04" and boss_toasted == False:
            toaster('boss')
            boss_toasted = True
        # Every month 1st and 16 reset Abyss
        elif today_date == "01" or today_date == "16" and abyss_toasted == False:
            toaster("abyss")
            abyss_toasted = True
        # Every month 1st Paimon's shop reset
        elif today_date == "01" and paimon_toasted == False:
            toaster("paimon")
            paimon_toasted = True

        ## Reset restriction
        if daily_notification_state == "0":
            normal_toasted = True
        else:
            if hour != hour:
                normal_toasted = False

        if advanced_notification_state == "0":
            resin_toasted = True
            boss_toasted = True
            abyss_toasted = True
            paimon_toasted = True
        else:
            if current_weekday == "Tue":
                boss_toasted = False
            elif today_date == "02" or today_date == "17":
                abyss_toasted = False
                paimon_toasted = False
      
def notifier():
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
    
    image = PIL.Image.open(current_path + "\Image\Paimon.png")
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
    

