# from tkinter import *
# from tkinter import ttk
# import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ctypes import windll
import sqlite3
from PIL import Image, ImageTk
from threading import Thread
import os

# import test_notic

class NotificationFrame(ttk.LabelFrame):

    def __init__(self, master, *args, **kargs):
        super().__init__(master, *args, **kargs)

        self.master = master
        # import win32com.shell.shell as shell
        # commands = 'schtasks /create /sc ONSTART /tn "Genshin Helper Notification" /tr "C:/Users/Jiahe31/AppData/Local/Programs/Python/Python311/python.exe c:/Users/Jiahe31/Desktop/CSP1123-GenshinHelper/test_notic.py"'
        # shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+commands)
        # os.system('schtasks /u /create /sc ONSTART /tn "Genshin Helper Notification" /tr "C:/Users/Jiahe31/AppData/Local/Programs/Python/Python311/python.exe c:/Users/Jiahe31/Desktop/CSP1123-GenshinHelper/test_notic.py"')

        self.s = ttk.Style()
        self.s.configure('fontt.TLabel', font=("Georgia", 15))
        self.s.configure('infoFont.TLabel', font=("TkDefaultFont", 8))
        self.label = ttk.Label(text="Notification", style="fontt.TLabel")
        self.config(labelwidget=self.label)

        self.notification_list = {}
        self.checkbox_nameVar = []

        buttonImage = Image.open(r'C:\Users\Jiahe31\Downloads\settings_20dp_FILL0_wght400_GRAD0_opsz20 (2) (2).png')
        self.buttonPhoto = ImageTk.PhotoImage(buttonImage)
        b = ttk.Button(self, image=self.buttonPhoto, bootstyle="dark", takefocus=False, command=self.settings)
        b.grid(column=3, row=1, sticky=W)
    

        # ttk.Button(self, text="SCRIPT NOT RUNNING", bootstyle='danger', takefocus=False, command=self.service).grid(column=4, row=1, sticky=W, padx=20)

        # Add task and status to dict
        for data in self.database("fetch"):
            # print(data[1])
            self.notification_list[data[0]] = eval(data[1]) # Add items to dict 

        print(f"\n{self.notification_list}")

        

        self.create_checkbox(self)


    def database(self, action, statement=None):
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

        elif action == "others":
            self.DBcursor.execute(statement)
        
        self.DBconnection.commit()
        self.DBconnection.close()
        

    # Create multiple checkbox
    def create_checkbox(self, master):

        row_init = 2
        for task, status in self.notification_list.items():
            
            var = ttk.BooleanVar()
            var.set(status)

            if task == 'MAIN_SWITCH':
                self.switch = var
                self.main_switch = ttk.Checkbutton(self, text="Desktop Notification", bootstyle="round-toggle", command=self.on, variable=self.switch)
                self.main_switch.grid(column=1, row=1, padx=20, pady=(10, 20), columnspan=2, sticky=W)
                if self.switch.get() == False:
                    self.main_switch.config(command=self.on, variable=var)
                elif self.switch.get() == True:
                    self.main_switch.config(command=self.off, variable=var)
                    

            if task != 'MAIN_SWITCH':
                # print(var.get())
                print(self.switch.get())
                self.checkbox = ttk.Checkbutton(master, text=task, bootstyle="round-toggle", variable=var, state=DISABLED)
                self.checkbox.grid(column=2, row=row_init, padx=(30, 0), pady=5, sticky=W)

                if self.switch.get() == True:
                    self.checkbox.config(state=NORMAL)
                elif self.switch.get() == False:
                    self.checkbox.config(state=DISABLED)
                # Keep a refrence for checkbox value
                self.notification_list[task] = var
                # Add checkbox variable to a list for config
                self.checkbox_nameVar.append(self.checkbox)
                # if self.switch == False:
                #     self.checkbox.config(state=DISABLED)
                
                
                row_init += 1

    def on(self):
        print("\nON")
        self.main_switch.config(command=self.off)
        for checkboxName in self.checkbox_nameVar:
            checkboxName.config(state=NORMAL)

        self.database("others", f"UPDATE notification SET Status = 'True' WHERE rowid = 1")

        import win32com.shell.shell as shell
        import subprocess
        create_schtasks = 'schtasks /create /sc ONSTART /tn "Genshin Helper Notification" /tr "C:/Users/Jiahe31/AppData/Local/Programs/Python/Python311/python.exe c:/Users/Jiahe31/Desktop/CSP1123-GenshinHelper/test_notic.pyw"'        
        # run_schtasks = 'schtasks /run /tn "Genshin Helper Notification"'
        shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+create_schtasks)
        # shell.ShellExecuteEx(lpVerb='runas',lpFile='cmd.exe', lpParameters='/c '+run)
        # subprocess.Popen(["python", "test_notic.pyw"], shell=True)
        subprocess.Popen("python test_notic.pyw", shell=True)

        


    def off(self):
        print("\nOFF")
        self.main_switch.config(command=self.on)
        for checkboxName in self.checkbox_nameVar:
            checkboxName.config(state=DISABLED)

        self.database("others", f"UPDATE notification SET Status = 'False' WHERE rowid = 1")

    def settings(self):
        settings = ttk.Toplevel()
        settings.title("Notification Settings")
        settings.geometry("500x300+406+209")

        # type = ttk.LabelFrame(settings, text="Type of notification")
        # type.grid(column=1, row=1, padx=10, pady=10, ipadx=300, ipady=300)
        self.startupVar = ttk.BooleanVar(value=True)
        ttk.Label(settings, text="Settings", font=("Georgia", 15)).grid(column=1, row=1, sticky=W, padx=20, pady=20)
        self.startup = ttk.Checkbutton(settings, text="  Start at startup.", bootstyle="round-toggle", variable=self.startupVar, command=self.startup)
        self.startup.grid(column=1, row=2, sticky=W, padx=20, pady=(10, 5))
        ttk.Label(settings, text="ON:  Start notification script in background when pc startup.", font=("Georgia", 7)).grid(column=1, row=3, sticky=W, padx=30, columnspan=5)
        ttk.Label(settings, text="OFF: Start notfication script in background only if Genshin Helper is open.", font=("Georgia", 7)).grid(column=1, row=4, sticky=W, padx=30, pady=(0, 10), columnspan=5)
        ttk.Label(settings, text="Daily Notification Time (24 Hrs)").grid(column=1, row=5, sticky=W, padx=20, pady=10)
        self.timeVar = ttk.StringVar(value='0')
        time = ttk.Spinbox(settings, width=3, textvariable=self.timeVar, from_=0,to=23) # , textvariable=pass
        time.grid(column=2, row=5, sticky=W)
        ttk.Checkbutton(settings, text="Remind activity when game is launched.", bootstyle="round-toggle").grid(column=1, row=6, sticky=W, padx=20, pady=10)

        

    

    def startup(self):
        print(self.startupVar.get())
        if self.startupVar.get() == False:
            pass
            # test_notic.startup(self.startupVar.get())












def main():

    windll.shcore.SetProcessDpiAwareness(1)

    root = ttk.Window(themename='themee')
    # root = ttk.Window()
    root.title("Notification")
    root.geometry("900x600+100+100")


    notic = NotificationFrame(root)
    notic.grid(column=1, row=1, padx=15, pady=10, ipady=100, ipadx=250)





    root.mainloop()

# thread = Thread(target=main)
# thread.start()
# thread.join()
main()
def test():
    os.system('python test_notic.pyw')
