from LogbookEntry import *
import os
from sys import exit, argv
import StringIO
import datetime


def getFilenames(dirName = "../LogbookEntries", LogBookFolder = "../Logbook"):
	filenames = []
	ignoreFiles = ["entry1.html", "SchoolsList.html"]
	for datestr in os.listdir(dirName):
		if datestr in ignoreFiles:
			continue #Skip over any files that should be ignored
		files = os.listdir('%s/%s'%(dirName, datestr))
		#Could have used a regexp here lol
		normalEntryFiles = [f for f in files if (f.upper().rfind("ENTRY") > -1 and f.upper().rfind(".HTM") > -1) and f.rfind('~') == -1]
		meetingEntryFiles = [f for f in files if (f.upper().rfind("MEETING") > -1 and f.upper().rfind(".TXT") > -1) and f.rfind('~') == -1]
		filenames = filenames + ["%s/%s/%s"%(dirName, datestr, f) for f in (normalEntryFiles + meetingEntryFiles)]
	return filenames


if __name__ == '__main__':
	if len(argv) < 3:
		print "Usage: python ReplaceLabels.py <currentName> <newName>"
		exit(0)
	currName = argv[1]
	newName = argv[2]
	for f in getFilenames():
		fin = open(f, 'r')
		lines = fin.readlines()
		fin.close()
		changed = False
		tags = []
		if len(lines) >= 3:
			tags = lines[2].split("Tags: ")[1]
			tags = [t.strip() for t in tags.split(",")]
			for i in range(0, len(tags)):
				t = tags[i]
				if t.upper() == currName.upper():
					tags[i] = newName
					changed = True
		if changed:
			tagsLine = "Tags: "
			for i in range(0, len(tags)):
				if i > 0:
					tagsLine = tagsLine + ", "
				tagsLine = tagsLine + tags[i]
			tagsLine = tagsLine + "\n"
			lines[2] = tagsLine
			print tagsLine
			fout = open(f, 'w')
			for line in lines:
				fout.write(line)
