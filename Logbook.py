from LogbookEntry import *
import os
from sys import exit, argv
import StringIO
import datetime

class Logbook(object):
	#dirName is the directory that holds the folders with the logbook entries
	#LogbookFolder is the root of the directory that holds the generated HTML files
	#It is assumed that dirName and LogbookFolder are at the same level
	def __init__(self, dirName = "../LogbookEntries", LogBookFolder = "../Logbook"):
		self.dirName = dirName
		self.LogBookFolder = LogBookFolder
		self.entries = {} #"date string" => [entry1, entry2, ...]
		self.tags = {}
		for datestr in os.listdir(dirName):
			if not datestr in self.entries:
				self.entries[datestr] = []
			files = os.listdir('%s/%s'%(dirName, datestr))
			#Could have used a regexp here lol
			files = [f for f in files if (f.upper().rfind("ENTRY") > -1 and f.upper().rfind(".HTM") > -1) and f.rfind('~') == -1]
			for f in files:
				entry = LogbookEntry()
				entry.initFromHTMLFile("%s/%s/%s"%(dirName, datestr, f))
				self.entries[datestr].append(entry)
	
	def writeDateEntryHTML(self, fout, datestr):
		ymd = [int(x) for x in datestr.split('-')]
		date = datetime.date(ymd[0], ymd[1], ymd[2])
		fout.write('<tr><td><h2><a href = \'%s/%s\'>%s</a></h2></td></tr>\n'%(self.dirName, datestr, date.strftime("%A %B %d, %Y")))		
	
	def writeSubEntryHTMLBegin(self, fout, entry):
		fout.write('<tr><td><a href = \'%s/%s\'>%s</a></td><td>'%(self.dirName, entry.filename, entry.description))
	
	def writeSubEntryHTMLEnd(self, fout):
		fout.write('</td></tr>\n')
	
	def writeTagLinkHTML(self, fout, tag, counts = -1):
		if counts == -1:
			fout.write('<a href = \'%s.html\'>%s</a> '%(tag, tag))
		else:
			fout.write('<a href = \'%s.html\'>%s (%i)</a> '%(tag, tag, counts))
	
	def writeTagCountsHTML(self, fout):
		fout.write('<h2><b>Tags</b></h2>\n')
		fout.write('<ul>\n')
		for tag in self.tags:
			fout.write('<li>')
			self.writeTagLinkHTML(fout, tag, self.tags[tag])
			fout.write('</li>\n')
		fout.write('</ul>\n')
	
	#Writes out the main page as an HTML file and also fills in the 'tags' set
	def generateMainpageHTML(self):
		fout = open('%s/index.html'%self.LogBookFolder, 'w')
		fout.write('<html>\n<body>\n')
		
		tableout = StringIO.StringIO()
		tableout.write('<table border = \'1\'\n')
		entriesRevOrder = [x for x in self.entries]
		entriesRevOrder.reverse()
		for datestr in entriesRevOrder:
			self.writeDateEntryHTML(tableout, datestr)
			for entry in self.entries[datestr]:
				self.writeSubEntryHTMLBegin(tableout, entry)
				for tag in entry.tags:
					if not tag in self.tags:
						self.tags[tag] = 0
					self.tags[tag] = self.tags[tag]+1
					self.writeTagLinkHTML(tableout, tag)
				self.writeSubEntryHTMLEnd(tableout)
		tableout.write('</table>\n');
		tablestring = tableout.getvalue()
		tableout.close()
		
		self.writeTagCountsHTML(fout)
		fout.write(tablestring)
		fout.write('</body>\n</html>\n')
	
	def generateTagHTMLPages(self):
		for tag in self.tags:
			fout = open('%s/%s.html'%(self.LogBookFolder, tag), 'w')
			fout.write('<body>\n<html>\n<h1><center>Entries Tagged with <b><u>%s</u></b></h1>\n<h2><a href = \'index.html\'> <-- Back to all entries</a></h2></center>\n'%(tag))
			fout.write('<table border = \'1\'\n');
			entriesRevOrder = [x for x in self.entries]
			entriesRevOrder.reverse()
			for datestr in entriesRevOrder:
				dateContainsTag = False
				for entry in self.entries[datestr]:
					if tag in entry.tags:
						dateContainsTag = True
						break
				if dateContainsTag:
					self.writeDateEntryHTML(fout, datestr)
					for entry in self.entries[datestr]:
						if tag in entry.tags:
							self.writeSubEntryHTMLBegin(fout, entry)
							for tag in entry.tags:
								self.writeTagLinkHTML(fout, tag)
							self.writeSubEntryHTMLEnd(fout)
			fout.write('</table\n');
			fout.write('</body>\n</html>\n')
			fout.close()			
	
	def generateAllHTMLFiles(self):
		self.generateMainpageHTML()
		self.generateTagHTMLPages()	
	
if __name__ == '__main__':
	if len(argv) >= 3:
		logbook = Logbook(argv[1], argv[2])
		logbook.generateAllHTMLFiles()
	else:
		logbook = Logbook()
		logbook.generateAllHTMLFiles()
