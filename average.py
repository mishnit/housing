
import pdb
import MySQLdb
import matplotlib.pyplot as plot

# Run the SQL.
SQL = '''
'''

def createPlot(axes,color,connection,query):
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
	axes.plot(dates,values,color)

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
	query = '''
	select listdate,
		list
	from houses
	where listdate is not null
		and list is not null
	order by listdate
	'''
	createPlot(axes,'ro-',connection,query)

	# Add listed properties.
	query = '''
	select date, average from (
		select x.listdate date, avg(y.list) average
		from houses x, houses y
		where x.id>=20 and x.id between y.id and y.id+19
		group by x.id
		order by x.id
	) data
	order by date
	'''
	createPlot(axes,'go-',connection,query)

	# Plot the data.
	figure.autofmt_xdate()
	plot.show()

	# Close the connection.
	connection.close()

if __name__ == '__main__':
	main()
