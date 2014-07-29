from LogbookEntry import *
import os
from sys import exit, argv
import StringIO
import datetime
import configFunctions

class Logbook(object):
	#dirName is the directory that holds the folders with the logbook entries
	#LogbookFolder is the root of the directory that holds the generated HTML files
	#It is assumed that dirName and LogbookFolder are at the same level
	def __init__(self, dirName = "../LogbookEntries", LogBookFolder = "../Logbook"):
		self.dirName = dirName
		self.LogBookFolder = LogBookFolder
		self.entries = {} #"date string" => [entry1, entry2, ...]
		self.tags = {}
		self.ignoreFiles = configFunctions.getIgnoredFiles()
		for datestr in os.listdir(dirName):
			if datestr in self.ignoreFiles:
				continue #Skip over any files that should be ignored
			if not datestr in self.entries:
				self.entries[datestr] = []
			files = os.listdir('%s/%s'%(dirName, datestr))
			#Could have used a regexp here lol
			normalEntryFiles = [f for f in files if (f.upper().rfind("ENTRY") > -1 and f.upper().rfind(".HTM") > -1) and f.rfind('~') == -1]
			for f in normalEntryFiles:
				entry = LogbookEntry()
				entry.initFromHTMLFile("%s/%s/%s"%(dirName, datestr, f))
				self.entries[datestr].append(entry)
			
			files = os.listdir('%s/%s'%(dirName, datestr))
			meetingEntryFiles = [f for f in files if (f.upper().rfind("MEETING") > -1 and f.upper().rfind(".TXT") > -1) and f.rfind('~') == -1]
			for f in meetingEntryFiles:
				entry = LogbookEntry()
				entry.initMeetingFromTXTFile("%s/%s/%s"%(dirName, datestr, f))
				self.entries[datestr].append(entry)				
	
	def writeDateEntryHTML(self, fout, datestr):
		ymd = [int(x) for x in datestr.split('-')]
		date = datetime.date(ymd[0], ymd[1], ymd[2])
		fout.write('<tr><td colspan = \"3\"><h2><a href = \'%s/%s\'>%s</a></h2></td></tr>\n'%(self.dirName, datestr, date.strftime("%A %B %d, %Y")))		
	
	def writeSubEntryHTMLBegin(self, fout, entry):
		entryName = entry.filename.split("/")[-1]
		entryName = entryName.split(".")[0]
		entryName = entryName.upper()
		filename = ""
		if entry.meetingFilename:
			filename = "%s/%s/%s"%(self.dirName, entry.datestr, entry.meetingFilename)
		else:
			filename = "%s/%s"%(self.dirName, entry.filename)
		fout.write('<tr><td><a href = \'%s\'>%s</a></td><td>%s</td><td>'%(filename, entryName, entry.description))
	
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
		tagList = [x for x in self.tags]
		tagList.sort()
		for tag in tagList:
			fout.write('<li>')
			self.writeTagLinkHTML(fout, tag, self.tags[tag])
			fout.write('</li>\n')
		fout.write('</ul>\n')
	
	#Writes out the main page as an HTML file and also fills in the 'tags' set
	def generateMainpageHTML(self):
		fout = open('%s/index.html'%self.LogBookFolder, 'w')
		fout.write('<html>\n<body>\n')
		
		tableout = StringIO.StringIO()
		tableout.write('<table border = \'1\'>\n')
		entriesRevOrder = [x for x in self.entries]
		entriesRevOrder.sort()
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
		entriesRevOrder = [x for x in self.entries]
		entriesRevOrder.sort()
		entriesRevOrder.reverse()
		for thisTag in self.tags:
			fout = open('%s/%s.html'%(self.LogBookFolder, thisTag), 'w')
			fout.write('<body>\n<html>\n<h1><center>Entries Tagged with <b><u>%s</u></b></h1>\n<h2><a href = \'index.html\'> <-- Back to all entries</a></h2></center>\n'%(thisTag))
			fout.write('<table border = \'1\'>\n');
			for datestr in entriesRevOrder:
				dateContainsTag = False
				for entry in self.entries[datestr]:
					if thisTag in entry.tags:
						dateContainsTag = True
						break
				if dateContainsTag:
					self.writeDateEntryHTML(fout, datestr)
					for entry in self.entries[datestr]:
						if thisTag in entry.tags:
							self.writeSubEntryHTMLBegin(fout, entry)
							for tag in entry.tags:
								self.writeTagLinkHTML(fout, tag)
							self.writeSubEntryHTMLEnd(fout)
			fout.write('</table>\n');
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
