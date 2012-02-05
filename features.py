import pdb
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

	# Add properties that have 4 bedrooms.
	features = ['Gas Fireplace',
		'Master Bedroom Ensuite',
		'Patio(s)',
		'Main Floor Laundry',
		'Separate Dining Room',
		'Family Room',
		'Rec Room',
		'Central Air',
		'Fenced Yard',
		'Water Softener',
		'Whirlpool',
		'Central Vac',
		'Cold Room/Cellar',
		'Alarm System',
		'Satellite Dish',
		'TV Cable',
		'Year-Round Road Access',
		'Year-Round Living',
		'Air Exchanger',
		'Walk-Out Basement',
		'Den/Office',
		'Handicap Provisions',
		'Lawn Sprinkler System',
		'Workshop',
		'In-Ground Pool',
		'Main Floor Master Bedroom',
		'Inlaw Suite',
		'Heating Stove',
		'Hot Tub',
		'Exercise Room',
		'Carpet Free',
		'Backs on Greenbelt',
		'Sauna',
		'Lovely 3 bedroom',
		'gleaming hardwood floors',
		'open concept lr.',
		'Auto-Garage Door/Remotes',
		'Walk-in Closet',
		'Dishwasher',
		'Refrigerator',
		'Stove',
		'Microwave',
		'Washer',
		'Dryer',
		'Wood Fireplace',
		'Deck(s)',
		'Shed',
		'Inside Entry (from Garage)',
		'Bathroom-Main Floor 2 Piece',
		'Freezer',
		'Above-Ground Pool',
		'Hi-Speed Internet',
		'On-Ground Pool',
		'Games Room',
		'Bathroom-Main Floor 3 Piece or More',
		'Pool-Equipment',
		'Bathroom-Rough-In',
		'Intercom',
		'Oriented to Seniors',
		'Detached Workshop',
		'Water Heater Owned',
		'Bathroom-Ensuite Privilege',
		'Security System',
		'Electric Fireplace',
		'Seasonal Road Access',
		'Separate Heating Controls',
		'Central Vac Rough-In']

	for feature in features:
		labels.append(feature)
		query = '''
		select %i, h.list
		from houses h, features f
		where h.list is not null
			and h.bedrooms = 4
			and h.bathrooms = 3
			and h.id = f.house_id
			and f.feature = '%s'
			and listdate between MAKEDATE(2011,01) and MAKEDATE(2012,01)
		''' % (len(labels), feature)
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
