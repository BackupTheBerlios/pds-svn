#! /usr/bin/python
# -*- coding: utf8 -*-
#
# backends.py is a part of PythonDesktopSearch
# PythonDesktopSearch is under the term of GPL
# (c) by SigMA <sigmahlm@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License.
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details. You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

# Dieses Modul stellt alle Backendtypen zu Verfügung
# Unterstützten werden sollen:
    # > cPickle / pickle
    # > mySQL
    # > SQLite
#
# Unterstützt werden schon:
    #    Backend         | Command  | Status
    # > cPickle / pickle | pickle   | fertig
    # > SQLite           | sqlite   | alpha - keine Suchanfrage

try:
    import cPickle as pickle
except ImportError:
    print "pyindexer konnte cPickle nicht finden! Es wird nun das langsamere pickle benutzt!"
    import pickle
import sqlite, os, lyp, config
from rt_search import *



class IndexHeader:
    def __init__(self, root_directory):
        self.root = root_directory
        self.timestamp = int(time.time())

class backend:
    def __init__(self, typ):
        # ToDo
            # mysql
        # / ToDo
        typ = config.backend
        self.support = ["pickle","sqlite"] # dynamischer machen ^^
        self.open_index = 0
        if typ in self.support:
            self.backend = typ
            
    def opendb(self):
        """
        Öffnet eine DB Schnittstelle
        Benötigt für sqlite
        """
        if self.backend == "sqlite":
            if not os.path.exists(config.index_file):
                # Erstellt die Tabelle
                file(config.index_file, "w")
                self.con = sqlite.connect(config.index_file)
                self.cur = self.con.cursor()
                self.cur.execute('CREATE TABLE pds(file VARCHAR(100), keywords VARCHAR(50))')
            else:
                self.con = sqlite.connect(config.index_file)
                self.cur = self.con.cursor()
                
    def writedb(self, db):
        """
        Fügt die im Indexer erstellte db in das Backend ein
        """
        # das db schaut wie folgt aus:
        ## IndexHeader(root_verzeichniss), self.files, self.keywords
        if self.backend == "pickle":
            pickle.dump(db, file(config.index_file, "w"),-1)   # Schreibt die DB
        elif self.backend == "sqlite":
            count = 0
            for i in db[1]:
                self.cur.execute("INSERT INTO pds(file, keywords) VALUES ('%s', '%s')" %(i,lyp.liste2string(db[2][count])))
                count += 1
            self.con.commit() # ab hier stehen die Änderungen in der DB
            
    def closedb(self):
        """
        Schließt die bestehende Verbindung
        und löscht die Index Variablen
        """
        try:
            del self.keywords
            del self.files
            del self.header
        except:
            pass
        self.open_index = 0
        
    def search(self, anfrage):
        res = []       
        if self.backend == "pickle":
            if self.open_index == 0: # Wenn Index noch nicht geöffnet,
                try:
                    self.header, self.files, self.keywords = pickle.load(file(config.index_file, "r",-1)) # dann lade Index
                    self.open_index = 1
                except IOError:
                    lyp.cout("Konnte keine Index Datei finden! Suche nun mit der Echtzeitsuche!")
            if self.open_index == 1:
                keywords = self.keywords # -|  o n l y
                files = self.files       # -| t h r 3 3
                speed_len = len          # -| Sp33d H4ck
                filecount = 0
                for e in keywords:
                    for i in e:
                        if speed_len(anfrage.findall(i)) >= 1:
                            hit = files[filecount]
                            res.append(hit)
                    filecount += 1
            else:
                
                rt = rt_searcher()
                res = rt.search(config.root_directory,anfrage)
        
        elif self.backend == "sqlite":
            self.cur.execute("SELECT * FROM pds WHERE keywords = \"%s\"" % anfrage)
            res = self.cur.fetchall()
            print res
            
        return(res)

# (c) by SigMA 2006
# under the term of GPL v2
