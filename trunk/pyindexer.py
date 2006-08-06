#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# Der Indexer der PythonDesktopSearch
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
# Die Keywords werden dynamischen von dem passenden Handler generiert
# alle Handler liegen in ./handler und können beliebig erweitert werden!

# IMPORT
# Python:
import os
import re
import time
import mimetypes
from os.path import join, getsize
import sys
import thread


try:
    import psyco
    psyco.profile()
except:
    pass


# / Python

# extra
import handler
from lyp import *
import config
from backends import *
# / extra
# / IMPORT

# ToDo
# > Blacklist Ordner gar nicht scannen! >> Speed
# >> Idee für Geschwindigkeit
    # For Schleifen bauen die immer
        # open Thread(argument) machen
    ## mal abklären, ob das gut ist^^

class IndexHeader:
    def __init__(self, root_directory):
        self.root = root_directory
        self.timestamp = int(time.time())

class Indexer:
    """
    Indexer der PythonDesktopSearch
    """
    def __init__(self):
        self.warteliste = []
        self.keywords = []
        self.threads = 0
        self.do = 0
#        try:
#           self.files, self.oldkeywords = pds.load_index (config.index_file)[0]
#        except:
        self.files, self.oldkeywords = [], []
    
    def scan_with_threads(self, arg, dirname, files):
        self.warteliste.append((arg, dirname, files))
        if self.do == 0:
            print "Start Thread"
            self.do = 1
            thread.start_new_thread(self._thread_scan, ())
        
    def _thread_scan(self):
        """
        Diese Funktion arbeitet die Warteschlange
        mit X Threads ab
        """
        while self.do == 1:
            for i in self.warteliste:
                if self.threads <= config.threads:
                    self.threads += 1
                    thread.start_new_thread(self._makelist, i)
                    self.warteliste.remove(i)
                

    def _makelist(self, arg, dirname, files):
        if self._check_bw_lists("", dirname):
            keywords = self.keywords # |- Speed
            filesback = self.files   # |- Hack
            for i in files:
                if not self._check_bw_lists(i, dirname):
                    continue
                key = []
                filename = join (dirname, i)
                # \todo Per Timestamp nach Änderung fragen und gegebenfalls Handler
                #       aufrufen
#                if filename in filesback:
#                    break
                filesback.append(filename)
                filetype = mimetypes.guess_type(i)
                try:
                    key = handler.filetypes[filetype[0]](filename) #öffnet den Handler
                except:
                    pass
                key.append(i)
                keywords.append(key)
            self.keywords = keywords # |- Ende Speed
            self.files = filesback   # |-    Hack
            self.threads -= 1
            del keywords             # |- Myll
            del filesback            # |- Myll
            

    def scan(self, root = config.root_directory):
        if config.threads != 0:
            os.path.walk(root, self.scan_with_threads, "")

            self.do = 0
        else:
            os.path.walk(root, self._makelist, "")
        return (IndexHeader(root), self.files, self.keywords)

    def _check_bw_lists(self, filename, directory):
        res = 1
        s = os.path.join(directory, filename)
        for i in config.blacklist:
            if re.search(i, s):
                res = 0
                for j in config.whitelist:
                    if re.search(j, s):
                        res = 1
                        break
        return res
        
if __name__ == "__main__":
    cout("Stellen Sie bitte sicher, dass sie den Indexer mit ROOT Rechten gestartet haben! \
    Drücken Sie sonst [STRG] + [C] zum Abbrechen um ihn erneut mit ROOT Rechten zu starten!","hinweis")
    backend = backend("pickle") # Setzt das Backend
    backend.opendb()            # Öffnet die DB
    
    starttime = time.time() # Startet die Uhr

    index = Indexer()       # Definiert den Indexer
    db = index.scan()       # startet den Scan Forgang
    backend.writedb(db)
    backend.closedb()
    
    try:
        os.remove(config.cache_file)
    except:
        pass
    end = time.time() - starttime   # Endet die Zeit nahme

    cout(str(len(index.files)) + " Dateien indexiert")
    cout(str(getsize(config.index_file)) + " Bytes geschrieben")
    cout("Insgesamt " + str(round (end, 2)) + " Sekunden")
