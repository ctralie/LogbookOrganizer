import sys, traceback

class LogbookEntry(object):
	def __init__(self):
		self.datestr = "01-01-1969"
		self.date = [0, 0, 0]
		self.description = "Description"
		self.tags = []
		self.filename = ""
		self.meetingFilename = None
	
	def initFromHTMLFile(self, filename):
		try:
			self.filename = filename
			self.datestr = filename.split('/')[-2]
			self.date = [int(x) for x in self.datestr.split('-')]
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
		except Exception as e:
			print("***Problem with %s\n%s***\n\n"%(filename, e))
			traceback.print_exc(file=sys.stdout)
	
	def initMeetingFromTXTFile(self, filename):
		try:
			self.filename = filename
			self.filename = filename
			self.datestr = filename.split('/')[-2]
			self.date = [int(x) for x in self.datestr.split('-')]
			fin = open(filename, 'r')
			#For a meeting the first three lines are always
			#filename
			#Description: This is a short description
			#Tags: Organizational, Imager, DHS
			self.meetingFilename = fin.readline()
			self.description = fin.readline().split("Description: ")[1]
			tags = fin.readline().split("Tags: ")[1]
			self.tags = [x.strip().upper() for x in tags.split(',')]
			fin.close()
		except Exception as e:
			print("***Problem with %s\n%s***\n\n"%(filename, e))
			traceback.print_exc(file=sys.stdout)
