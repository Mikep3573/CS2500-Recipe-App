import sqlite3 # included in standard python distribution
import csv

con = sqlite3.connect('olympic.db')

cur = con.cursor()

#remove table during subsequent runs
cur.execute("DROP TABLE IF EXISTS olympic;")

#create the table
create_table = '''CREATE TABLE olympic('ID','Name',	'Sex',	'Age',	'Height',	'Weight'	,'Team',	'NOC',	'Games'	,'Year',	'Season',	'City',	'Sport',	'Event'	,'Medal')'''
cur.execute(create_table)

#load from csv
file = open('olympic.csv')
contents = csv.reader(file)
header = next(contents)  ## throw away headers
print(contents)

insert_records = "INSERT INTO olympic('ID','Name','Sex','Age','Height','Weight','Team','NOC','Games','Year','Season','City','Sport','Event','Medal') VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
cur.executemany(insert_records, contents)

delete_blank_lines = "DELETE FROM olympic where ID = ''"
cur.execute(delete_blank_lines)
con.commit()
con.close()