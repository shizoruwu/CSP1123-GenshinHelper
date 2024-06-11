import time
import datetime
import win11toast
import sqlite3
import multiprocessing
import pystray
import PIL.Image
import os

current_path = os.path.abspath(os.getcwd())

def fetch():
    DBconnection = sqlite3.connect("genshindata.db")
    DBcursor = DBconnection.cursor()

    data = DBcursor.execute("SELECT * FROM tasks") # Read
    data = data.fetchall() # Get
    amount = 0
    for i in range(len(data)):
        if data[i][1] == 'False':
            amount += 1

    global hours
    hours = DBcursor.execute("SELECT Status FROM notification WHERE Notification = 'DAILY_NOTIFICATION_TIME'")
    hours = hours.fetchall()

    global notic
    notification = DBcursor.execute("SELECT Notification FROM notification WHERE Status = '1' AND rowid > 4")
    notification = notification.fetchall()
    notic = []
    for i in range(len(notification)):
        notic.append(notification[i][0])   

    DBconnection.close()
    return amount

def toaster(type):
    msg = ""
    characters = 'Keqing, Nahida'
    weapons = "Kagura's Verity"

    checkin = "Hi! It's the time to check-in!\n"
    todo = f"You have {fetch()} To-Do Tasks left. "
    character = f"You planned to upgrade:\n- Characters: {characters}\n"

    resin = "You resin is about to overflow!!"
    boss = "Weekly bosses has been reset today."
    abyss = "Abyss bosses has been reset today."
    paimon = "Paimon's Shop has been reset today."
    

    for notification in notic:
        match notification:
            case "Daily Check-in":
                msg += checkin
            case "To-Do Tasks":
                msg += todo
            case "Characters planned to be upgraded":
                msg += character

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

def click(a):
    import GenshinHelper_Main

def start_service(hour):
    # Add a zero get a proper 24 Hrs Format
    hour = hour[0][0]
    if int(hour) >= 0 and int(hour) < 10:
        hour = "0" + hour[0][0]

    while True:
        current_time = datetime.datetime.now().strftime("%H")
        weekday = datetime.datetime.now().strftime("%a")
        date = datetime.datetime.now().strftime("%d")
        print(current_time)

        time.sleep(1)
        # Daily notification
        if current_time == hour:
            toaster('normal')
            time.sleep(3600) # 1h-3600s 1m-360s
        # Every Monday 4am reset weekly bosses
        elif weekday == "Mon" and current_time == "04":
            toaster('boss')
        # Every month 1st and 16 reset Abyss
        elif date == "01" or date == "16":
            toaster("abyss")
        # Every month 1st Paimon's shop reset
        elif date == "01":
            toaster("paimon")
      
def notifier():
    fetch()
    start_service(hours)
    # toaster('abyss')
    
def quit(pid):
    tray.stop()
    os.popen(f'taskkill /pid {pid} /f')

### System tray
def sys_tray(pid):
    global tray
    image = PIL.Image.open(current_path + "\Materials\Mora.png")
    tray = pystray.Icon("Tray", image, menu=pystray.Menu(
        pystray.MenuItem("Exit", lambda:quit(pid=pid))
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
    
    

