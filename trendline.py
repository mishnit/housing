
import random
import MySQLdb
import matplotlib.pyplot as plot

def randomColor():
	result = '%x' % random.randint(0, 16777215)
	if len(result) == 5:
		return '#0'+result
	elif len(result) == 4:
		return '#00'+result
	return '#'+result

def createPlot(axes,style,connection,query):
	# Query for the data.
	cursor = connection.cursor()
	cursor.execute(query)
	results = cursor.fetchall()
	cursor.close()

	# Reformat the data.
	dates = []
	values = []
	for date, value in results:
		# Sometimes date comes out as None. Not sure why.
		if date and value:
			dates.append(date)
			values.append(float(value))

	# Create the new axes.
	color = randomColor()
	axes.plot(dates,values,style,color=color)

def main():
	# Connect to the database.
	connection = MySQLdb.connect (host = 'localhost',
				user = 'root',
				passwd = '80017001',
				db = 'housing')

	# Create the figure.
	figure = plot.figure()
	axes = figure.add_subplot(111)

	# Add sold properties.
	for year in range(1995,2012):
		query = '''
		select solddate, sold
		from houses
		where sold is not null
			and solddate between MAKEDATE(%s,01) and MAKEDATE(%s,01)
			and bedrooms between 4 and 4
			and bathrooms between 3 and 3
		order by solddate
		''' % (year, year+1)
		createPlot(axes,'-',connection,query)

	# Plot the data.
	figure.autofmt_xdate()
	plot.show()

	# Close the connection.
	connection.close()

if __name__ == '__main__':
	# Seed random numbers.
	random.seed

	main()

