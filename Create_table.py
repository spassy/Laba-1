import sqlite3

conn = sqlite3.connect('skill.db')
#drop = "DROP TABLE skillbox ()"
sql = "CREATE TABLE skillbox (id INTEGER PRIMARY KEY, Profession TEXT, Description TEXT, Price TEXT, Time TEXT)"
#sql = 'SELECT * FROM skillbox'
cursor = conn.cursor()

#cursor.execute(drop)
cursor.execute(sql)

#res = cursor.fetchall()

#for r in res:
#    print(r)

conn.close()
