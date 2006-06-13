#! /usr/bin/python
# -*- coding: utf-8 -*-
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
import os, re, time, cPickle
from db import *
from config import *
# / IMPORT

# ToDo
# > Keywords bauen (im mom ist das Filename)
# > Blacklist Ordner gar nicht scannen! >> Speed
# >> Idee für Geschwindigkeit
    # For Schleifen bauen die immer
        # open Thread(argument) machen
    ## mal abklären, ob das gut ist^^

class indexer:
    """
    Indexer der PythonDesktopSearch
    """
    def __init__(self):
        self.files = []
        self.keywords = []
    def makelist(self, arg, dirname, files):
        if self.checkblacklist(dirname) == 1:
            keywords = self.keywords # |- Speed
            filesback = self.files   # |- Hack
            for i in files:
                filesback.append(dirname+os.sep+i)
                key = i
                keywords.append(key)
            self.keywords = keywords # |- Speed
            self.filesback = files   # |- Hack
            del keywords
            del files
    def scan(self):
        print "start walking ..."
        stopwalk = time.time()
        os.path.walk("/", self.makelist, "")
        endwalk = time.time() - stopwalk
        print "... Fertig nach "+str(endwalk)+" Sekunden"
        print "Schreibe index.pds  ..."
        stopwalk = time.time()
        dblist = []
        dblist.append(self.files)
        dblist.append(self.keywords)
        ffile = open("index.pds", "w")
        cPickle.dump(dblist, ffile,-1)
        ffile.close()
        endwalk = time.time() - stopwalk
        print "... Fertig nach "+str(round(endwalk, 3))+" Sekunden"
        print str(len(self.files))+" Dateien indexiert"
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
