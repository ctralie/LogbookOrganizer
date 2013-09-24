LogbookOrganizer
================

This is a collection of scripts I use all the time to help manage my work as I do my Ph.D.  The basic idea is to just stitch together a bunch of HTML files and folders that contain content, and to date and tag these files and folders so I can find related things quickly.  This makes it easy to manage a lot of projects at once, and it allows me to find things quickly by tags.

Not only does this program help me when I need to show my work to people, it will also provide me with a record of what it took to get a Ph.D.  I encourage you to use it so you can do the same!


Getting Started
---------------
First download the script from Github, either using git clone or downloading the .zip file off of Github.

Now note the directory structure (which should *NOT* be changed)
* Logbook: This directory will store the main page (index.html) and all of the tag pages (every file in this folder is automatically generated).  Click on index.html in this folder to view the logbook.  The index.html page contains a list of tag hyperlinks at the top, and a table of entries below.  Each entry is under a date heading.  Clicking on the date hyperlink will bring you to the folder that contains all entries and files under that date.  Clicking on the entry hyperlink will bring you to the HTML page for that entry.

* LogbookAdmin: This directory contains the scripts that are used to generate the HTML code in the *Logbook* folder.  When you would like to generate your logbook for the first time, or you have made any changes and would like to update your logbook, simply change to the *LogbookAdmin* directory and run the `Logbook.py` file.

~~~~~ bash
python Logbook.py
~~~~~

* LogbookEntries: This directory contains all of the content that you will create.  I have included as a sample 4 separate entries on 3 different days, as well as a template entry "entry1.html".  See the next section for how to make a logbook entry

Making a New Entry
------------------
To create a new entry, you first need to create a new directory in the *LogbookEntries* directory which has the date of that entry.  The directory must be named as follows: `YYYY-MM-DD`.  So for example, if I had an entry on January 12, 2010, I would create the directory `2013-01-12`.

Once you have created the directory, you must create a file called *entry1.html* to represent the first entry on that date.  Subsequent entries on the same day can be called entry2.html, entry3.html, etc.  But they must all follow the convention entryX.html, starting with 1.  I usually start by copying the template file entry1.html into my new folder and editing that.

Now to make the entry and inform the logbook how to deal with it, there is a bit of data you need to fill out at the top of your entry1.html file.  The sample *entry1.html* file in *LogbookEntries* shows exactly how to do this.  Repeated here for convenience:
~~~~~ HTML
<!--LOGBOOK ORGANIZER INFO
Description: This is a short description for a sample entry
Tags: SampleEntry, OtherTag
!-->
~~~~~
* The first and fourth lines of that file are comments which you should not edit.

* The second line contains a description of the entry which will show up in the logbook's index.html file and any tag files that contain this entry.  It's a short description that helps you figure out what the entry is all about before you click on it.  Be sure to keep the description all on one line.

* The third line contains all of the tags of the entry separated by commas.  The tags help you to file and find entries that are similar to each other, and any given entry can have many tags.  I have tried to show examples of this in the samples LogbookEntries I have provided on Github.

The rest of the content in that file from line 5 on is totally up to you.  It's an HTML file, so you will have to adhere to HTML syntax standards.  But you can do a lot with HTML, which I've tried to highlight in my sample entries.  Everything from embedding pictures, to making hyperlinks, to even embedding videos.

There is one more little option you have in this logbook which is to have "meeting entries."  Instead of making an *entryX.html* file, you make a *meeting1.txt* file which links to another file (usually PDF or PPTX).  This is for linking to presentations on a particular day.  I have many, many meetings every week, so this was a useful feature for me.  An example is shown in the LogbookEntry samples.

And That's It!
--------------
Once you are done all of this, you should be good to go!  Just make those new entries and watch the logbook come to life!  In all seriousness, this program has helped me significantly to become more organized in grad school and I think it's saved me a lot of time.  Whenever I have meetings I just click on the appropriate tags and copy stuff from my recent entries into powerpoints.
