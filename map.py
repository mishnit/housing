from pylab import *
import MySQLdb
import random

# Constants.
MAX_CIRCLE_SIZE = 100
MIN_CIRCLE_SIZE = 5

def randomColor():
	result = '%x' % random.randint(0, 16777215)
	if len(result) == 5:
		return '#0'+result
	elif len(result) == 4:
		return '#00'+result
	return '#'+result

def normalize(value,maxValue,minValue,maxTarget,minTarget):
	'''
	Normalizes the given values with respect to the target.
	'''
	return float(maxTarget)*(float(value)-float(minValue))/(float(maxValue) - float(minValue)) + float(minTarget)

def plotData(minValue,maxValue,connection,query):
	# Query for the data.
	cursor = connection.cursor()
	cursor.execute(query)
	results = cursor.fetchall()
	cursor.close()

	# Generate the plot.
	for result in results:
		(x,y,value) = result
		color = randomColor()
		size = normalize(value,maxValue,minValue,MAX_CIRCLE_SIZE,MIN_CIRCLE_SIZE)
		scatter(x,y, c=color, s=size, alpha=0.3, edgecolors=None)

def getLimits(connection):
	'''
	Returns the max, min of the list price.
	'''
	# Create a cursor.
	cursor = connection.cursor()

	# Query for the data.
	query = '''\
	select max(list),
		min(list)
	from houses
	where list is not null
		and latitude is not null
		and longitude is not null
	'''
	cursor.execute(query)
	(maxValue, minValue) = cursor.fetchone();

	# Close the cursor.
	cursor.close()

	# Return the values.
	return (maxValue, minValue)

def main():

	# Connect to the database.
	connection = MySQLdb.connect (host = "localhost",
				user = "root",
				passwd = "80017001",
				db = "housing")

	# Get the limits of the list price.
	maxValue, minValue = getLimits(connection)

	# Load the data from the database.
	for year in range(1995,2012):
		query = '''
		select latitude,
			longitude,
			list
		from houses
		where list is not null
			and latitude is not null
			and longitude is not null
			and listdate between MAKEDATE(%s,1) and MAKEDATE(%s,1)
		''' % (year, year+1)
		plotData(minValue,maxValue,connection,query)

	# Plot the data.
	grid(True)
	show()

	# Close the connection.
	connection.close ()

if __name__ == '__main__':
	main()

