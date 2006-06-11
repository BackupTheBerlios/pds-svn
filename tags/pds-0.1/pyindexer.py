#! /usr/bin/python
#coding: utf-8
#
# Der Indexer der pythonDesktopSearch
# (c) by SigMA 2006
# -----------------------------------
# Dieser Indexer sucht alle Dateien raus
# und speichert sie in der Datenbank, die
# wie folgt ausschaut
# (mit Beispiel)
#
# FILE URL               | Keywords
# /home/USER/wichtig.abw | wichtig, abw, seeehr wichtig [..]
#
# Die Keywords sollen dynamisch generiert werden^^

# IMPORT
import os, re, time
#from ID3 import *
from db import *
from config import *
# import cPickle as pickle
# / IMPORT

# ToDo
# > Keywords bauen (im mom ist das Filename)
# > Blacklist Ordner gar nicht scannen! >> Speed
# >> Idee für Geschwindigkeit
    # For Schleifen bauen die immer
        # open Thread(argument) machen
    ## mal abklären, ob das gut ist^^

class indexer:
    def __init__(self):
        # Hier wird später geschaut, wo er als letztes war
        self.files = []
        self.keywords = []
        self.db = pydsdb()
    def makelist(self, arg, dirname, files):
        if self.checkblacklist(dirname) == 1:
            for i in files:
                self.files.append(dirname+os.sep+i)
                # Hier kommt später das Keyword-Tool rein
                # nach dem Prinzip:
                # > if XFileType:
                    # generate keyword
                # else: key = i
                key = i
                self.keywords.append(key)
    def scan(self):
        self.db.sql("DROP TABLE pds",1)
        print "start walking ..."
        stopwalk = time.time()
        os.path.walk("/", self.makelist, "")
        endwalk = time.time() - stopwalk
        print "... Fertig nach "+str(endwalk)+" Sekunden"
        print "Schreibe DB ..."
        stopwalk = time.time()
        count = 0
        self.db.sql("CREATE TABLE pds(file VARCHAR(100), keywords VARCHAR(100))")
        lstr = str               # -|
        files = self.files       # -| Speed Hack
        keywords = self.keywords # -|
        del self.files
        del self.keywords
        for i in xrange(len(files)):
            try:
                # replace("'","\\'") geht irgendwie nicht mit dem gewünschten
                # erfolg
                self.db.add(files[i],keywords[i])
            except:
                pass # Wenn ein Fehler > ignoriere ihn^^
            if count == commit:
                self.db.do()
                count = 0
            count += 1
        self.db.do()
        endwalk = time.time() - stopwalk
        print "... Fertig nach "+str(endwalk)+" Sekunden"
        print lstr(len(files))+" Dateien indexiert"
        del files
        del keywords
    def checkblacklist(self, dirname):
        to_return = 1
        for black in blacklist:
            if dirname.find(black) >= 1:
                to_return = 0
        return(to_return)
        
if __name__ == "__main__":
    starttime = time.time()
    searchbot = indexer()
    searchbot.scan()
    end = time.time() - starttime
    print "Insgesamt "+str(end)+" Sekunden"
