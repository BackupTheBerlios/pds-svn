#! /usr/bin/python
#coding: utf-8

# PythonDesktopSearch is under the GPL
# (c) by SigMA 2006 - http://www.sigma.us.ms

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License.
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details. You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

# ToDo
# Zeile 84
# >> schauen ob es auch KeyInsensitiv geht

from lyp import *
from db import *
from config import * 
import re, time, cPickle, os, sys

class pydesksearch:
    def __init__(self):
        self.db = pydsdb()
        self.keywords = []
        self.files = []
        starttime = time.time()
        if os.path.exists("file.cache") == False or os.path.exists("keywords.cache") == False:
            cout("Keine Cache Datei gefunden! Erstelle neues SearchIndex")
            self.new_search_index()
            if cache == True:
                self.cache("save")
        else:
            cout("Cache Datei gefunden!")
            self.cache("load")
        end = time.time() - starttime
        print "In "+str(end)+" Sekunden"
    def stopwatch(self,command):
        if command == "go":
            self.startzeit = time.time()
        elif command == "stop":
            return(time.time()-self.startzeit)

    def new_search_index(self, asdf="wasistsechsmultipliziertmitneun"):
        self.files = []
        self.keywords = []
        self.stopwatch("go")
        alldata = self.db.showall()
        for i in alldata:
                self.files.append(i[0])
                self.keywords.append(i[1])
        del alldata
        cout("In "+str(self.stopwatch("stop"))+" Sekunden Daten ausgelesen")
        if cache == True and asdf == "new_index":
            self.cache("save")
        cout("Neues SuchIndex erstellt")
    def cache(self, what):
        """
        Diese Funktion cached die DB in 2 Dateien
        keywords.cache
        files.cache
        so können die Daten schneller ausgelesen werden
        """
        if what == "save":
            cout("Starte schreiben von Cache Datei ...")
            self.stopwatch("go")
            ffile = open("file.cache", "w")
            fkey = open("keywords.cache", "w")
            cPickle.dump(self.files, ffile,-1)
            cPickle.dump(self.keywords, fkey,-1)
            cout("Daten in "+str(self.stopwatch("stop"))+" Sekunden geschrieben!")
        elif what == "load":
            ffile = open("file.cache", "r",-1)
            fkey = open("keywords.cache", "r",-1)
            self.files = cPickle.load(ffile)
            self.keywords = cPickle.load(fkey)
        ffile.close()
        fkey.close()
    def search(self, anfrage):
        anfrage = anfrage.rstrip()
        page = []
        # Hier wird die Anfrage bearbeitet!
        files = self.files       # -| Speed
        keywords = self.keywords # -| Hack
        speed_len = len          # -|
        cout("\nDurchsuche ... ")
        filecount = 0
        treffer = 0
        starttime = time.time()
        for i in keywords:
            if speed_len(re.compile(anfrage,re.IGNORECASE).findall(i)) >= 1:
                page.append(files[filecount].replace(anfrage,RED+anfrage+RESET))
                treffer += 1
            filecount += 1
        cout("... fertig\n")
        del keywords
        del files
        end = time.time() - starttime
        count = 0
        tmp_count = 0
        cout("||"+"="*25+"PythonDesktopSearch"+"="*25+"||")
        for i in page:
            cout(i)
            tmp_count += 1
            if tmp_count >= treffer_page:
                print ">> Enter für die nächsten "+str(treffer_page)+" Treffer <<"
                raw_input()
                tmp_count = 0
        cout("||"+"="*25+"PythonDesktopSearch"+"="*25+"||")
        cout("""||"""+"""="""*38+"""||\n||\t"""+str(filecount) + """ Datein durchsucht\t||
||\t"""+str(treffer) + """ Dateien waren ein Treffer\t||
||\tIn """+str(round(end,3))+""" Sekunden\t\t||\n||"""+"""="""*38+"""||""")
        del page
        
if __name__ == "__main__":
    # Überprüfe, ob es Python 2.4 ist
    if sys.version_info[0] != 2 or sys.version_info[1] < 4:
        cout("Die PythonDesktopSearch läuft nur auf Python2.4 Laden Sie sich \
bitte die aktuelle Version von http://www.python.org","hinweis")
        sys.exit("Exit: Nicht die aktuelle Version")
    # / Ende
    argv = sys.argv
    def new_cache():
         os.unlink("file.cache")
         os.unlink("keywords.cache")
         cout("Erstelle neuen SearchIndex") 
         pds.new_search_index("new_index")
         cout("Fertig")
    if len(argv) <= 1:
        argv.append("-help")
    if argv[1] == "--new_cache":
        pds = pydesksearch()
        new_index()
    elif argv[1] == "--search":
        pds = pydesksearch()
        pds.search(liste2string(argv[2:]))
    elif argv[1] == "-cmd":
        pds = pydesksearch()
        while 1:
            cout("\nIhre Suchanfrage (in RE)?")
            anfrage = raw_input("?> ")
            if anfrage == "/new_cache":
                new_cache()
            elif anfrage == "/quit":
                break
            elif anfrage == "":
                pass
            else:
                pds.search(anfrage)
            cout("Bis zum nächsten mal!", "info")
    elif argv[1] == "-gpl":
        f = open("gpl.txt", "r")
        print f.read()
        f.close()
    elif argv[1] == "--help" or argv[1] == "-?" or argv[1] == "-h":
        cout("\n\tPythonDesktopSearch"+RESET+" Commandline\n   (c) by SigMA 2006 \
under the term of the GPL\n\t\tversion: "+version+"\
\n\n--search SUCHWORT\tSucht nach SUCHWORT\n\
--new_cache\t\terstellt neue Cache Dateien\n-cmd\t\t\tStartet mit einer \
Commandline\n-gpl\t\t\tZeigt ihnen die GPLv2\n")
    else:
        cout("\nUnbekannter Befehl\nVersuchen Sie --help für mehr Informationen\n")
