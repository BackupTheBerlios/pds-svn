#! /usr/bin/python
# -*- coding: utf-8 -*-

# PythonDesktopSearch is under the GPL
# (c) by SigMA

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License.
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details. You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307

from lyp import *

try:
    import cPickle as pickle
except ImportError:
    import pickle

import re, os, sys
from os.path import join, exists

from pyindexer import IndexHeader

import config

def load_index(filename):
        """
        Diese Funktion lädt den Index und schreibt ihn in die lokalen Variablen
        files
        self.keywords
        """
        return pickle.load(file(filename, "r",-1))

def do_color(s, req):
    if config.color:
        matches = re.findall(req, s)
        for i in matches:
            s = s.replace(i, RED + i + RESET)
    return s

class Finder:
    def __init__(self):
        try:
            self.header, self.files, self.keywords = load_index(config.index_file)
        except IOError:
            cout("Index " + config.index_file + " konnte nicht geöffnet werden\n")
            cout("Erstellen Sie bitte zuerst einen Index mit dem pyindexer bevor Sie die Suche starten!")
            sys.exit(1)
    
    def search(self, anfrage):
        """
        Die Suchfunktion. Diese Funktion kann eigentlich für jedes
        beliebige Programm benutzt werden, welches eine Suchfunktion
        für die Festplatte braucht
        """
        anfrage = anfrage.rstrip()
        anfrage = re.compile(anfrage, re.IGNORECASE)
        res = []
        # Hier wird die Anfrage bearbeitet!
        files = self.files       # -| Speed
        keywords = self.keywords # -| Hack
        speed_len = len          # -|
        filecount = 0
        for e in keywords:
            for i in e:
                if speed_len(anfrage.findall(i)) >= 1:
                    hit = files[filecount]
                    res.append(hit)
            filecount += 1
        return res

    def search_xml(self, req):
        # \todo Echtes XML (DOM oder SAX)
        res = u"""<?xml version="1.0"?>
<result rootdir="%s" timestamp="%s">\n""" % (self.header.root, self.header.timestamp)
        for i in self.search(req):
            res += unicode ("\t<entry>%s</entry>\n" % i, errors = "ignore")
        res += u"</result>"
        return res

