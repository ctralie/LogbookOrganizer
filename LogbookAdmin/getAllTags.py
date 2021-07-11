from LogbookEntry import *
import os
from sys import exit, argv
import StringIO
import datetime

if __name__ == '__main__':
	#dirName is the directory that holds the folders with the logbook entries
	#LogbookFolder is the root of the directory that holds the generated HTML files
	#It is assumed that dirName and LogbookFolder are at the same level
	dirName = "../LogbookEntries"
	LogBookFolder = "../Logbook"
	dirName = dirName
	LogBookFolder = LogBookFolder
	entries = {} #"date string" => [entry1, entry2, ...]
	tags = {}
	ignoreFiles = ["entry1.html", "SchoolsList.html"]
	ignoreTags = ["DHS", "Imager", "ImagerMeeting"]
	for i in range(len(ignoreTags)):
		ignoreTags[i] = ignoreTags[i].upper()
	fout = open("logbookTags.txt", "w")
	for datestr in os.listdir(dirName):
		if datestr in ignoreFiles:
			continue #Skip over any files that should be ignored
		if not datestr in entries:
			entries[datestr] = []
		files = os.listdir('%s/%s'%(dirName, datestr))
		#Could have used a regexp here lol
		normalEntryFiles = [f for f in files if (f.upper().rfind("ENTRY") > -1 and f.upper().rfind(".HTM") > -1) and f.rfind('~') == -1]
		for f in normalEntryFiles:
			HTMLFilename = "%s/%s/%s"%(dirName, datestr, f)
			fin = open(HTMLFilename, 'r')
			lines = fin.readlines()
			tags = []
			description = ""
			if len(lines) >= 3:
				description = lines[1]
				tags = lines[2].split("Tags: ")[1]
				tags = [t.strip() for t in tags.split(",")]
			fin.close()
			doOutput = True
			for tag in tags:
				if tag.upper() in ignoreTags:
					doOutput = False
					print("Ignoring " + HTMLFilename)
					break
			if doOutput:
				for tag in tags:
					fout.write("%s "%tag.upper())
	fout.close()
