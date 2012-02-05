
import random
import MySQLdb
import matplotlib.pyplot as plot

def randomColor():
	result = '%x' % random.randint(0, 16777215)
	if len(result) < 6:
		return '#0'+result
	return '#'+result

def createPlot(axes,connection,query):
	# Query for the data.
	cursor = connection.cursor()
	cursor.execute(query)
	results = cursor.fetchall()
	cursor.close()

	# Reformat the data.
	keys = []
	values = []
	keyAverage = 0
	valueAverage = 0
	for key, value in results:
		# Sometimes key comes out as None. Not sure why.
		if key and value:
			keys.append(key)
			values.append(float(value))
			keyAverage += key
			valueAverage += value

	if len(keys) == 0:
		return

	keyAverage = float(keyAverage)/float(len(keys))	
	valueAverage = float(valueAverage)/float(len(values))	

	# Create the new axes.
	color = randomColor()
	axes.plot(values,keys,'x',color=color)
	axes.plot((valueAverage,),(keyAverage,),'o',color=color)

def main():
	# Seed random numbers.
	random.seed()

	# Connect to the database.
	connection = MySQLdb.connect (host = 'localhost',
				user = 'root',
				passwd = '80017001',
				db = 'housing')

	# Create the figure.
	figure = plot.figure()
	axes = figure.add_subplot(111)
	labels = []

	# Add properties that have 3 bedrooms.
	label = '3 bedrooms'
	labels.append(label)
	query = '''
	select %i, list
	from houses
	where list is not null
		and bedrooms = 3
	''' % len(labels)
	createPlot(axes,connection,query)

	# Add properties that have 4 bedrooms.
	label = '4 bedrooms'
	labels.append(label)
	query = '''
	select %i, list
	from houses
	where list is not null
		and bedrooms = 4
	''' % len(labels)
	createPlot(axes,connection,query)

	# Add properties that have 2 bathrooms.
	label = '2 bathrooms'
	labels.append(label)
	query = '''
	select %i, list
	from houses
	where list is not null
		and bathrooms = 2
	''' % len(labels)
	createPlot(axes,connection,query)

	# Add properties that have 3 bathrooms.
	label = '3 bathrooms'
	labels.append(label)
	query = '''
	select %i, list
	from houses
	where list is not null
		and bathrooms = 3
	''' % len(labels)
	createPlot(axes,connection,query)

	# Add properties that have 4 bathrooms.
	label = '4 bathrooms'
	labels.append(label)
	query = '''
	select %i, list
	from houses
	where list is not null
		and bathrooms = 4
	''' % len(labels)
	createPlot(axes,connection,query)

	# Setup the axes.
	axes.set_ylim(0,len(labels)+1)
	axes.set_yticks(range(1,len(labels)+1))
	axes.set_yticklabels(labels)

	# Plot the data.
	plot.show()

	# Close the connection.
	connection.close()

if __name__ == '__main__':
	main()
