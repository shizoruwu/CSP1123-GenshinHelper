import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
import sqlite3
import subprocess
import win32com.shell.shell as shell
from ctypes import windll


class NotificationFrame(ttk.LabelFrame):

    def __init__(self, master, *args, **kargs):
        super().__init__(master, *args, **kargs)

        self.master = master

        self.s = ttk.Style()
        self.s.configure('fontt.TLabel', font=("Georgia", 15))
        self.s.configure('infoFont.TLabel', font=("TkDefaultFont", 8))
        self.label = ttk.Label(text="Notification", style="fontt.TLabel")
        self.config(labelwidget=self.label)

        self.notification_list = {}
        self.checkbox_nameVar = []

        for data in self.database("fetch"):
            self.notification_list[data[0]] = data[1]
        
        print(f"\n{self.notification_list}")
        self.create_list()
        self.time.bind('<Return>', self.set_time)

    def database(self, action="others", statement=None):
        # Connect db
        self.DBconnection = sqlite3.connect("genshindata.db")
        self.DBcursor = self.DBconnection.cursor()
        # Create a table if not exists
        self.DBcursor.execute("CREATE TABLE IF NOT EXISTS notification(Notification, Status)")

        if action == "fetch":
            # Read and get values from db
            data = self.DBcursor.execute("SELECT * FROM notification") # Read
            self.data = data.fetchall() # Get
            return self.data
        
        elif action == "fetch_PID":
            data = self.DBcursor.execute("SELECT Status FROM notification WHERE rowid >= 4 AND rowid <= 5")
            return data.fetchall()

        elif action == "others":
            self.DBcursor.execute(statement)
        
        self.DBconnection.commit()
        self.DBconnection.close()

    def create_list(self):
        row_init = 3

        for data, status in self.notification_list.items():
            var = ttk.IntVar()
            var.set(status)

            # Grid notification switches and time setting
            if data == "DAILY_NOTIFICATION":
                self.daily_notification_status = var
                print(self.daily_notification_status.get())
                self.daily_notification = ttk.Checkbutton(self, text="Desktop Notification", bootstyle="round-toggle", variable=self.daily_notification_status)
                self.daily_notification.grid(column=1, row=1, padx=20, pady=(10, 0), columnspan=2, sticky=W)
                if self.daily_notification_status.get() == 1: # True
                    self.daily_notification.config(command=lambda: self.off("normal"))
                else: 
                    self.daily_notification.config(command=lambda: self.on("normal"))

            elif data == "ADVANCED_NOTIFICATION":
                self.advanced_notification_status = var
                self.advanced_notification = ttk.Checkbutton(self, text="Notification (Advanced)", bootstyle="round-toggle", variable=self.advanced_notification_status)
                self.advanced_notification.grid(column=1, row=6, padx=20, pady=(20, 10), columnspan=2, sticky=W)
                if self.advanced_notification_status.get() == 1: # True
                    self.advanced_notification.config(command=lambda: self.off("advanced"))
                else:
                    self.advanced_notification.config(command=lambda: self.on("advanced"))

            elif data == "DAILY_NOTIFICATION_TIME":
                self.timeVar = ttk.StringVar(value=var.get())
                label = ttk.Label(self, text="Daily Notification Time (24 Hrs Format)")
                label.grid(column=1, row=2, sticky=W, padx=(30, 0), pady=(5, 0))
                self.time = ttk.Spinbox(self, width=3, textvariable=self.timeVar, from_=0,to=23) # , textvariable=pass
                self.time.grid(column=2, row=2, sticky=W, pady=(10, 0))
                ToolTip(self.time, text="Press Enter to Apply new value.")
                ToolTip(label, text="Press Enter to Apply new value.")

            if data != "DAILY_NOTIFICATION" and data != "DAILY_NOTIFICATION_TIME" and data != "ADVANCED_NOTIFICATION" and data != "PID_NOTIFIER" and data != "PID_TRAY":
                if data == "Resin Overflow Reminder":
                    row_init += 2
                self.checkbox = ttk.Checkbutton(self, text=data, variable=var, bootstyle="round-toggle", command=self.state)
                self.checkbox.grid(column=1, row=row_init, padx=(30, 0), pady=5, sticky=W)
                row_init += 1
                self.notification_list[data] = var
                self.checkbox_nameVar.append(self.checkbox)
                for checkbox in self.checkbox_nameVar[:3]:
                    if  self.daily_notification_status.get() == 1:
                        checkbox.config(state=NORMAL)
                    else:
                        checkbox.config(state=DISABLED)
                for checkbox in self.checkbox_nameVar[3:]:
                    if  self.advanced_notification_status.get() == 1:
                        checkbox.config(state=NORMAL)
                    else:
                        checkbox.config(state=DISABLED)

        print(self.notification_list)
                        
    def on(self, type):
        if type == "normal":
            print("normal on")
            self.daily_notification.config(command=lambda: self.off("normal"))
            for checkbox in self.checkbox_nameVar[:3]:
                    checkbox.config(state=NORMAL)
            self.database("others", "UPDATE notification SET Status = '1' WHERE Notification = 'DAILY_NOTIFICATION'")
            subprocess.Popen("pythonw notifier.pyw", shell=True)
        elif type == "advanced":
            print("advanced on")
            self.advanced_notification.config(command=lambda: self.off("advanced"))
            for checkbox in self.checkbox_nameVar[3:]:
                    checkbox.config(state=NORMAL)
            self.database("others", "UPDATE notification SET Status = '1' WHERE Notification = 'ADVANCED_NOTIFICATION'")
            subprocess.Popen("pythonw notifier.pyw", shell=True)

    def off(self, type):
        if type == "normal":
            print("normal off")
            self.daily_notification.config(command=lambda: self.on("normal"))
            for checkbox in self.checkbox_nameVar[:3]:
                    checkbox.config(state=DISABLED)
            self.database("others", "UPDATE notification SET Status = '0' WHERE Notification = 'DAILY_NOTIFICATION'")
            pid = self.database("fetch_PID")
            subprocess.Popen(f'taskkill /pid {pid[0][0]} /f', shell=True)
            subprocess.Popen(f'taskkill /pid {pid[1][0]} /f', shell=True)
        elif type == "advanced":
            print("advanced off")
            self.advanced_notification.config(command=lambda: self.on("advanced"))
            for checkbox in self.checkbox_nameVar[3:]:
                    checkbox.config(state=DISABLED)
            self.database("others", "UPDATE notification SET Status = '0' WHERE Notification = 'ADVANCED_NOTIFICATION'")
            pid = self.database("fetch_PID")
            subprocess.Popen(f'taskkill /pid {pid[0][0]} /f', shell=True)
            subprocess.Popen(f'taskkill /pid {pid[1][0]} /f', shell=True)

    def state(self):
        for notifications in self.notification_list:
            if isinstance(self.notification_list[notifications], ttk.IntVar):
                connection = sqlite3.connect("genshindata.db")
                cursor = connection.cursor()
                cursor.execute("UPDATE notification SET Status = ? WHERE Notification = ?", (self.notification_list[notifications].get(), notifications,))
                connection.commit()
                connection.close()

    def set_time(self, a):

        def info(status=None):
            global info_label
            self.grid = False
            info_label = ttk.Label(self)
            info_label.grid(column=3, row=2, sticky=W, padx=10)
            if status == "success":
                info_label.config(text="New Value Saved!")
            elif status == "exceed":
                info_label.config(text="Invalid Value, Please type 0 to 23 only.", bootstyle="danger")
            else:
                info_label.config(text="Invalid Value/Type, Please type 0 to 23 (Integer) only.", bootstyle="danger")
            self.grid = True

        try:
            if self.grid == True:
                info_label.destroy()
                self.grid = False
            if int(self.time.get()) >= 0 and int(self.time.get()) <= 23:
                self.database("others", statement=f"UPDATE notification SET Status = {self.time.get()} WHERE Notification = 'DAILY_NOTIFICATION_TIME'")
                info("success")
            else:
                info("exceed")
        except:
            info()


    















def main():

    windll.shcore.SetProcessDpiAwareness(1)

    root = ttk.Window()
    # root = ttk.Window()
    root.title("Notification")
    root.geometry("900x600+100+100")

    notic = NotificationFrame(root)
    notic.grid(column=1, row=1, padx=15, pady=10, ipady=100, ipadx=250)

    root.mainloop()

if __name__ == '__main__':
    main()
