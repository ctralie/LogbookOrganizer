#Extract part of the current logbook and make a new logbook with only the entries
#with a particular tag
from LogbookEntry import *
import os
from sys import exit, argv
import StringIO
import datetime
import subprocess


def getFilenamesAndDirs(dirName = "../LogbookEntries", LogBookFolder = "../Logbook"):
    filesdirs = []
    ignoreFiles = ["entry1.html", "SchoolsList.html"]
    for datestr in os.listdir(dirName):
        if datestr in ignoreFiles:
            continue #Skip over any files that should be ignored
        files = os.listdir('%s/%s'%(dirName, datestr))
        #Could have used a regexp here lol
        normalEntryFiles = [f for f in files if (f.upper().rfind("ENTRY") > -1 and f.upper().rfind(".HTM") > -1) and f.rfind('~') == -1]
        meetingEntryFiles = [f for f in files if (f.upper().rfind("MEETING") > -1 and f.upper().rfind(".TXT") > -1) and f.rfind('~') == -1]
        filesdirs = filesdirs + [[datestr, f] for f in (normalEntryFiles + meetingEntryFiles)]
    return filesdirs

def executeCommand(command):
    print(command)
    subprocess.call(command)

if __name__ == '__main__':
    if len(argv) < 3:
        print("Usage: python makeSublogbook.py <tagName> <newDirectory>")
        exit(0)
    tagName = argv[1]
    copyLocDir = argv[2]
    entriesToCopy = set([])
    datesToCopy = set([])
    for finfo in getFilenamesAndDirs():
        [datestr, f] = finfo
        fin = open("../LogbookEntries/%s/%s"%(datestr, f), 'r')
        lines = fin.readlines()
        fin.close()
        changed = False
        tags = []
        if len(lines) >= 3:
            tags = lines[2].split("Tags: ")[1]
            tags = [t.strip() for t in tags.split(",")]
            for i in range(0, len(tags)):
                t = tags[i]
                if t.upper() == tagName.upper():
                    entriesToCopy.add("%s/%s"%(datestr, f))
                    datesToCopy.add(datestr)
                    break
    executeCommand(["mkdir", "%s/LogbookEntries"%copyLocDir])
    executeCommand(["mkdir", "%s/Logbook"%copyLocDir])
    executeCommand(["cp", "-R", "../LogbookAdmin", copyLocDir])
    #Recursive copy all directories
    for d in datesToCopy:
        executeCommand(["cp", "-R", "../LogbookEntries/%s"%d, "%s/LogbookEntries"%copyLocDir])
        #Delete all entries that don't have the label in question
        files = os.listdir("../LogbookEntries/%s"%d)
        normalEntryFiles = [f for f in files if (f.upper().rfind("ENTRY") > -1 and f.upper().rfind(".HTM") > -1) and f.rfind('~') == -1]
        for n in normalEntryFiles:
            if not "%s/%s"%(d, n) in entriesToCopy:
                executeCommand(["rm", "%s/LogbookEntries/%s/%s"%(copyLocDir, d, n)])
