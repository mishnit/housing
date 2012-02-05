
from sys import argv
from HTMLParser import HTMLParser
import MySQLdb
from datetime import date
from os import listdir
from os.path import join

INSERT_HOUSE = '''\
insert into houses (address,type,style,bedrooms,bathrooms,sold,list,area,subarea,near,age,basement,listdate,solddate,mbr)\
values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)\
'''
GET_LAST_HOUSE = '''\
select LAST_INSERT_ID();
'''
INSERT_FEATURE = '''\
insert into features (house_id,feature)\
values (%s,%s)\
'''

class house:
	'''
	A simple house.
	'''
	def __init__(self):
		'''
		Constructor.
		'''
		self.address = ''
		self.type = None
		self.style = None
		self.bedrooms = None
		self.bathrooms = None
		self.sold = None
		self.list = None
		self.area = None
		self.subarea = None
		self.near = None
		self.age = None
		self.basement = None
		self.listdate = None
		self.solddate = None
		self.mbr = None
		self.features = []

	def write(self):
		'''
		Writes the house to the database.
		'''
		connection = MySQLdb.connect (host = 'localhost',
					user = 'root',
					passwd = '80017001',
					db = 'housing')
		cursor = connection.cursor ()

		# Write the house.
		cursor.execute (INSERT_HOUSE,
		                (self.address.replace('\n','').strip(),
		                 self.type,
		                 self.style,
		                 self.bedrooms,
		                 self.bathrooms,
		                 self.sold,
		                 self.list,
		                 self.area,
		                 self.subarea,
		                 self.near,
		                 self.age,
		                 self.basement,
		                 str(self.listdate),
		                 str(self.solddate),
		                 self.mbr))

		# Get the house's id to write the features.
		cursor.execute(GET_LAST_HOUSE)
		houseId = cursor.fetchone()[0]

		# Add the features.
		for feature in self.features:
			cursor.execute(INSERT_FEATURE,(houseId,feature))

		cursor.close ()
		connection.close ()

class housingParser(HTMLParser):
	'''
	Parses MLS printouts.
	'''
	def __init__(self):
		'''
		Used to control data parsing based on the tag.
		'''
		HTMLParser.__init__(self)
		self.lastTag = None
		self.lastHeader = None
		# True if the upcoming data entry is bolded.
		self.isBold = False
		self.house = None
		# A counter for the number of address lines to expect.
		# There is no explicit header for addresses.
		self.addressLines = 0

	def handle_starttag(self,tag,attrs):
		'''
		Store the last tag and check for a bold tag, which indicates a header.
		'''
		# Store the last tag.
		self.lastTag = tag

		# Check for bolding.
		if len(attrs) > 0:
			for attr in attrs:
				key, value = attr
				if key == 'style':
					self.isBold = 'bold' in value

	def handle_data(self,data):
		'''
		Parse the data.
		'''
		# If this is a valid data entry.
		data = data.strip()
		if len(data) <= 0:
			return

		# Most tags with data are nobr tags.
		if self.lastTag == 'nobr':

			# If this is a bold entry, store it for the next hit.
			if self.isBold:
				if self.lastHeader == 'Address:':
					# Address is a continuous set of tags until we
					# hit price.
					if '$' in data:
						self.house.list = self.dollarValueToInt(data)
						self.lastHeader = None
					else:
						self.house.address += data
				elif data.startswith('MLS#: '):
					# The MLS number signals the start of a house.
					# If there is a house, write it to the database
					# and create a new one.
					if self.house:
						self.house.write()
					self.house = house()
					# The MLS number is encoded in the title.
					self.house.mls = data.replace('MLS#: ','')
					# Address follows the MLS number.
					self.lastHeader = 'Address:'
				else:
					# Store the header for later use.
					self.lastHeader = data

			# Just for clarity; these values aren't bolded.
			elif self.lastHeader:

				# If this is the type, store it for later.
				if self.lastHeader.startswith('Type'):
					self.house.type = data

				elif self.lastHeader.startswith('Style'):
					self.house.style = data

				elif self.lastHeader.startswith('Bed/Bath'):
					bedrooms,bathrooms = data.split('/',1)
					self.house.bedrooms = self.getNumberOfRooms(bedrooms)
					self.house.bathrooms = self.getNumberOfRooms(bathrooms)

				elif self.lastHeader.startswith('Area'):
					self.house.area = data

				elif self.lastHeader.startswith('Sub-Area'):
					if self.house.subarea:
						self.house.subarea += ' ' + data
					else:
						self.house.subarea = data

				elif self.lastHeader.startswith('Near'):
					self.house.near = data

				elif self.lastHeader.startswith('Age/Built'):
					self.house.age = data

				elif self.lastHeader.startswith('Basement'):
					self.house.basement = data

				elif self.lastHeader.startswith('Monthly Fee'):
					self.house.basement = data

				elif self.lastHeader.startswith('List Date'):
					self.house.listdate = self.getDate(data) 

				elif self.lastHeader.startswith('Sold Date'):
					self.house.solddate = self.getDate(data) 

				elif self.lastHeader.startswith('Sold Price'):
					self.house.sold = self.dollarValueToInt(data)

		# For some strange reason, features are stored in spans. If we kept
		# span tags with the normal nobr tags, our lastHeader section would
		# be rewritten; so they're kept separate.
		elif self.lastTag == 'span':

			if self.lastHeader and self.lastHeader.startswith('Features'):
				for feature in data.split(','):
					feature = feature.strip().replace('\n','')
					self.house.features.append(feature)

				# To make sure we don't keep going and get the rest
				# of the comments.
				self.lastHeader = None


	def getDate(self,data):
		'''
		Returns a date object based on the content of data.
		'''
		month, day, year = data.split('/',3)
		return date(int(year),int(month),int(day))

	def getNumberOfRooms(self,data):
		'''
		Sometimes the number of rooms can be a + b.
		'''
		if '+' in data:
			a,b = data.split('+',2)
			return int(a.strip()) + int(b.strip())
		else:
			return int(data)

	def dollarValueToInt(self,value):
		'''
		Converts a string dollar value to an int.
		'''
		return int(float((''.join([c for c in value if c.isdigit() or c == '.']))))

files = listdir(argv[1])
for filename in files:
	print filename
	parser = housingParser()
	with open(join(argv[1],filename),'r') as file:
		parser.feed(file.read())
		parser.house.write()

