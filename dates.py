
import pdb
import MySQLdb
import matplotlib.pyplot as plot

def createPlot(axes,color,label,connection,query):
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
	axes.plot(dates,values,color,label=label)

def main():
	# Connect to the database.
	connection = MySQLdb.connect (host = 'localhost',
				user = 'root',
				passwd = '80017001',
				db = 'housing')

	# Create the figure.
	figure = plot.figure()
	axes = figure.add_subplot(111)

	# Add listed properties.
	query = '''
	select listdate,
		list
	from houses
	where listdate is not null
		and list is not null
	order by listdate
	'''
	createPlot(axes,'go-','listed houses',connection,query)

	# Add sold properties.
	query = '''
	select solddate,
		sold
	from houses
	where solddate is not null
		and sold is not null
	order by solddate
	'''
	createPlot(axes,'ro-','sold houses',connection,query)

	# Add list-sold properties.
	query = '''
	select solddate,
		list-sold
	from houses
	where solddate is not null
		and sold is not null
	order by solddate
	'''
	createPlot(axes,'bo-','sold houses',connection,query)

	"""
	# Add properties close to my area.
	query = '''
	select solddate,
		sold
	from houses
	where sold is not null
		and solddate is not null
		and latitude > 43.48
		and longitude > -80.58
		and longitude < -80.54
	order by solddate
	'''
	createPlot(axes,'bo-','close houses',connection,query)
	"""

	# Plot the data.
	figure.autofmt_xdate()
	plot.show()

	# Close the connection.
	connection.close()

if __name__ == '__main__':
	main()
