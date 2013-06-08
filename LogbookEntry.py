
class LogbookEntry(object):
	def __init__(self):
		self.datestr = "01_01_1969"
		self.date = [0, 0, 0]
		self.description = "Description"
		self.tags = []
		self.filename = ""
	
	def initFromHTMLFile(self, filename):
		self.filename = filename
		self.datestr = filename.split('/')[-2]
		self.date = [int(x) for x in self.datestr.split('_')]
		fin = open(filename, 'r')
		#The first three lines are always
		#<!--LOGBOOK ORGANIZER INFO
		#Description: This is a short description
		#Tags: Organizational, Imager, DHS
		fin.readline()
		self.description = fin.readline().split("Description: ")[1]
		tags = fin.readline().split("Tags: ")[1]
		self.tags = [x.strip().upper() for x in tags.split(',')]
		fin.close()
