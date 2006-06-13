#! /usr/bin/python
# -*- coding: utf-8 -*-

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
        starttime = time.time()
        if os.path.exists("index.pds") == False:
            cout("Erstellen Sie bitte zuerst ein SearchIndex mit dem pyindexer\n\
Bevor Sie die Search starten!")
            sys.exit("Exit: Kein SearchIndex")
        else:
            cout("SearchIndex gefunden!")
            self.index("load")
        end = time.time() - starttime
        print "In "+str(end)+" Sekunden"
    def stopwatch(self,command):
        if command == "go":
            self.startzeit = time.time()
        elif command == "stop":
            return(time.time()-self.startzeit)
    def index(self, what):
        """
        Diese Datei lädt das Index und spaltet es
        in die beiden Variablen
        self.files
        self.keywords
        """
        ffile = open("index.pds", "r",-1)
        db = cPickle.load(ffile)
        self.files = db[0]
        self.keywords = db[1]
        ffile.close()
    def search(self, anfrage):
        """
        Die Suchfunktion. Diese Funktion kann eigentlich für jedes
        beliebige Programm benutzt werden, welches eine Suchfunktion
        für die Festplatte braucht
        """
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
                if color == True:
                    page.append(files[filecount].replace(anfrage,RED+anfrage+RESET))
                else:
                    page.append(files[filecount])
                treffer += 1
            filecount += 1
        cout("... fertig\n")
        del keywords
        del files
        seitenanzahl = len(page) / treffer_page
        aktuell_seite = 0
        end = time.time() - starttime
        count = 0
        tmp_count = 0
        cout("||"+"="*25+"PythonDesktopSearch"+"="*25+"||")
        for i in page:
            cout(i)
            tmp_count += 1
            if tmp_count >= treffer_page and show_page == True:
                aktuell_seite += 1
                print ">> Seite "+str(aktuell_seite)+" von "+str(seitenanzahl)+" Seiten <<"
                print ">> Enter für die nächsten "+str(treffer_page)+" Treffer <<"
                print ">> Q [enter] für ein Vorzeitiges Beenden der Ergebnisse <<"
                if raw_input() == "q" or raw_input=="Q":
                    break
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
    elif argv[1] == "--search" or argv[1] == "-s":
        pds = pydesksearch()
        pds.search(liste2string(argv[2:]))
    elif argv[1] == "-cmd":
        pds = pydesksearch()
        anfrage = " "
        while 1:
            if anfrage != "":
                cout("\nIhre Suchanfrage (in RE)? ('/quit' zum Beenden)")
            anfrage = raw_input("?> ")
            if anfrage == "/quit":
                break
            elif anfrage == "":
                pass
            else:
                pds.search(anfrage)
    elif argv[1] == "-gpl":
        f = open("gpl.txt", "r")
        print f.read()
        f.close()
    elif argv[1] == "--help" or argv[1] == "-?" or argv[1] == "-h":
        cout("""\n\tPythonDesktopSearch"+RESET+" Commandline
   (c) by SigMA 2006 under the term of the GPL
\t\tversion: """+version+"""
\n-s --search SUCHWORT\tSucht nach SUCHWORT
-cmd\t\t\tStartet mit einer Commandline
-gpl\t\t\tZeigt ihnen die GPLv2
\n""")
    else:
        cout("\nUnbekannter Befehl\nVersuchen Sie --help für mehr Informationen\n")
