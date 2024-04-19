import sqlite3


connection = sqlite3.connect('cities.db')
cursor = connection.cursor()
'''
cursor.execute("""CREATE TABLE IF NOT EXISTS cities (
                  city_id TEXT PRIMARY KEY,
                  city_name TEXT NOT NULL,
                  latitude REAL NOT NULL,
                  longitude REAL NOT NULL);""")

cursor.execute(""" INSERT INTO cities (city_id, city_name, latitude, longitude)
                   VALUES ('c637229a-bcdc-4c68-8459-85a6395e9ddc', 'Tokyo', 35.6895, 139.6917);""")
'''
cursor.execute("SELECT * FROM cities;")
connection.commit()
result = cursor.fetchall()
print(result)

cursor.close()
connection.close()
