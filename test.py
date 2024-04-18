import sqlite3

conn = sqlite3.connect('genshindata.db')
cur = conn.cursor()
cur.execute("SELECT Weapontype FROM Characterdata WHERE id=Amber")
weapon = cur.fetchone

print(weapon)