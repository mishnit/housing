import MySQLdb
from geopy import geocoders
import time

# Run the SQL.
connection = MySQLdb.connect (host = "localhost",
			user = "root",
			passwd = "80017001",
			db = "housing")
cursor = connection.cursor()
cursor.execute ('select id,address from houses')
results = cursor.fetchall()
cursor.close ()

# Parse the results and calculate their coordinates.
coder = geocoders.Google('ABQIAAAAvku0YOnYWepO69Y_ZfZi8xTjkcT51IQK3aHlLFb4XkdT5OAMGhTe6Q2SpV1Ovx7Uv078u2JU6bbnqQ')
locations = {}
for result in results:
	try:
		# Store the result.
		uid,address = result
		address = address.replace('#','').replace('-','')
		print address
		place, (latitude, longitude) = coder.geocode(address)  
		locations[uid] = (latitude,longitude)

	except Exception as exception:
		print exception

	# Don't dos the system.
	time.sleep(2)

# Store the results in the database.
cursor = connection.cursor()
for uid in locations:
	(latitude,longitude) = locations[uid]
	cursor.execute('update houses set latitude=%s, longitude=%s where id=%s',(latitude,longitude,uid))

# We're done entering the values.
cursor.close ()

# Close the db connection.
connection.close ()
