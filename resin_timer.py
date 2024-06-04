import tkinter as tk
import sqlite3
from tkinter import ttk
from datetime import datetime, timedelta
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

class resintimer(ttk.LabelFrame):
  def __init__(self, master, *args, **kargs):
    super().__init__(master, *args, **kargs)

    #resin timer features
    #self.geometry("800x600")
    #self.title("Resin Timer")
    clock_recorded = False

    #grid
    self.columnconfigure((0,1), weight = 1)
    self.rowconfigure((0,1,2,3), weight = 1)
    self.rowconfigure(4, weight = 8)
    self.rowconfigure(5, weight = 1)
    
    #features label
    resin_label = tk.Label(self, text="Enter your current Resin :")
    resin_label.grid(row=0, column=0, sticky="e")

    resin_label_box = tk.Entry(self)
    resin_label_box.grid(row=0, column=1, sticky="w")

    #result
    full_refill = tk.Label(self, text='Results:', font=('Helvetica',20))
    full_refill.grid(row=3, column=0, columnspan=2, sticky='sw')

    result_text = tk.Text(self, height=10, width=40)
    result_text.grid(row=4, column=0, columnspan=2)
    result_text.config(state="disabled")

    dbresult_label = tk.Label(self, text="")
    dbresult_label.grid(row=1, column=0, columnspan=2)

    #function to fetch data from db
    def fetch_data():
        cur.execute("SELECT * FROM resintimer")
        rows = cur.fetchall()
        display_text=""
        result_text.config(state="normal")
        result_text.delete(1.0, tk.END)
        for row in rows:
            display_text = f"Last recorded at {row[0]} with {row[1]} resins left.\n"

            clock = row[0]
            resin = row[1]
            time = str(row[2])
            new_minutes = row[3]
            #show results after rerun the code
            current_time = datetime.now()

            current_minutes = current_time.hour * 60 + current_time.minute

            stored_minutes = int(time[:2]) * 60 + int(time[2:4])

            if current_minutes >= stored_minutes:
                resin_time = current_minutes - stored_minutes
            else:
                resin_time = current_minutes + (24 * 60 - stored_minutes)
            current_resin = (resin_time // 8) + resin
            calculate_time(current_resin, new_minutes, resin)
        
        result_text.config(state="disabled")
        dbresult_label.config(text = display_text)

    #delete records after pressing refresh
    def delete_records():
        cur.execute("DELETE FROM resintimer")
        conn.commit()
        fetch_data()

    def confirm():
        try:
            result_text.config(state="normal")
            resin_amount = int(resin_label_box.get())

            if resin_amount < 0 or resin_amount > 160:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Number must be between 0 to 160")
                self.after(3000, fetch_data)
            else:
                clear()
                calculate_time(resin_amount=resin_amount)
        except ValueError:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Please fill in ONLY NUMBER!!!", "colour")
            result_text.tag_config("colour", foreground="red")
            self.after(3000, fetch_data)
        finally:
            result_text.config(state="disabled")

    #refresh
    def clear():
        global clock_recorded
        result_text.config(state="normal")
        result_text.delete(1.0, tk.END)
        result_text.config(state="disabled")
        delete_records()
        #reset clock_recorded to "False" so that if there are changes in resin_amount can be insert in db
        clock_recorded = False

    confirm_button = tk.Button(self, text="Confirm", command= confirm, width=15, height=2)
    confirm_button.grid(row=2, column=0, sticky='se')

    clear_button = tk.Button(self, text="Clear All", command = clear, width=15, height=2)
    clear_button.grid(row=2, column=1, sticky='sw', padx=(0,150))

    #function to calculate resin left
    def calculate_time(resin_amount=None, new_minutes=None, resin=None):
        global clock_recorded
        result_text.config(state="normal")
        try:
            if resin_amount is None:
                resin_amount = int(resin_label_box.get())
            if resin is None:
                resin = int(resin_label_box.get())
            if new_minutes is None:
                new_minutes = datetime.now().minute

            #input between 0-160
            if resin_amount <= 159:
                result_text.insert(tk.END, f"Your current resins: {resin_amount}\n")
                for i in range(20, 161, 20):
                    if resin_amount < i:
                        time_per_resin = 8
                        current_resin = i-resin_amount
                        minutes_needed = (current_resin) * time_per_resin
                        duration = timedelta(minutes=minutes_needed)
                        current_time = datetime.now()
                        new_time = current_time + duration
                        hours = minutes_needed // 60
                        a = new_minutes + (((i-resin)*8)%60)
                        if a >= 60:
                            a = a-60
                        if current_time.minute < a:
                            minute = a - current_time.minute
                        else:
                            minute = (a + 60) - current_time.minute
                        if resin_amount <= 159:
                            result_text.insert(tk.END, f"{i:03} resin in {hours:02}h {minute:02}min at {new_time.strftime('%I')}:{a:02} {new_time.strftime('%p')}\n")
                        else:
                            result_text.delete(1.0, tk.END)
                            result_text.insert(tk.END, f"Your resin is full")

                cur.execute("SELECT COUNT(*) FROM resintimer")
                count = cur.fetchone()[0]
                if count==0:
                    if not clock_recorded:   #check if the clock is recorded
                        current_time = datetime.now()
                        cur.execute("INSERT INTO resintimer (clock, resin, time, new_minutes) VALUES (?, ?, ?, ?)", (current_time.strftime("%d-%m-%Y %I:%M %p"), resin_amount, current_time.strftime("%H%M.%S"), current_time.minute))
                        conn.commit()
                        clock_recorded = True
            elif resin_amount >= 160:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Your resin is full")
        except ValueError:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Please fill in ONLY NUMBER!!!", "colour")
            result_text.tag_config("colour", foreground="red")
        finally:
            result_text.config(state="disabled")

    #clock
    #update clock every second
    def update_clock():
        current_time = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
        clock_label.config(text="Current Time: " + current_time)
        self.after(1000, update_clock)

    #clock label
    clock_label = tk.Label(self, text='')
    clock_label.grid(row=5, column=0, columnspan=1, sticky="sw")

    #connect db
    conn = sqlite3.connect('genshindata.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS resintimer(clock,resin)")

    #update results every minutes
    def update_result():
        fetch_data()
        current_time = datetime.now()
        next_minute = (60 - current_time.second) * 1000
        self.after(next_minute, update_result)

    #update clock every second
    update_clock()

    #fetch and display data
    fetch_data()
    update_result()

def main():
  windll.shcore.SetProcessDpiAwareness(1)

  root = ttk.Window()
  root.title("Character Search")
  root.geometry('1310x825')

  notic = resintimer(root)
  notic.grid(column=1, row=1, padx=15, pady=10, ipady=100, ipadx=250)

  root.mainloop()

if __name__ == '__main__':
  main()