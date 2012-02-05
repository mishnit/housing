import MySQLdb

# Constants.
SQL = 'select list,type,longitude,latitude from houses'

# Run the SQL.
connection = MySQLdb.connect (host = "localhost",
			user = "root",
			passwd = "31415692",
			db = "housing")
cursor = connection.cursor()
cursor.execute (SQL)
results = cursor.fetchall()
cursor.close ()
connection.close ()

print 'name,desc,latitude,longitude'

for result in results:
	list,type,longitude,latitude = result
	print list,',',
	print type,',',
	print longitude,',',
	print latitude,','
