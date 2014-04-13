from LogbookEntry import *
import os
from sys import exit, argv
import StringIO
import datetime

#Note: This script requires the program "html2text" to be installed
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
	os.popen3("touch logbookText.txt")
	os.popen3("rm logbookText.txt")
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
			print HTMLFilename
			os.popen3("html2text %s >> logbookText.txt"%HTMLFilename)
	os.popen3("html2text ../Logbook/index.html > logbookTextMain.txt")
