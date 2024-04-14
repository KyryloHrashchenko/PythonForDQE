import sqlite3


connection = sqlite3.connect('test.db')
cursor = connection.cursor()

cursor.execute("SELECT * FROM private_ad")
connection.commit()
result = cursor.fetchall()
print(result)

cursor.close()
connection.close()
