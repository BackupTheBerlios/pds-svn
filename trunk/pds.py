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
    
import re, os, sys, mimetypes
from os.path import join, exists

from pyindexer import IndexHeader

from backends import *

from rt_search import *

import config

def load_index(filename):
        """
        Diese Funktion lädt den Index
        """
        return pickle.load(file(filename, "r",-1))

def do_color(s, req):
    if config.color:
        matches = re.findall(req, s)
        for i in matches:
            s = s.replace(i, RED + i + RESET)
    return s

class Finder:
    def __init__(self, typ):
        #try:
        #    self.header, self.files, self.keywords = load_index(config.index_file)
        #except IOError:
        #    cout("Index " + config.index_file + " konnte nicht geöffnet werden\n")
        #    cout("Erstellen Sie bitte zuerst einen Index mit dem pyindexer bevor Sie die Suche starten!")
        #    sys.exit(1)
        self.backend = backend(config.backend)
        self.typ = typ
        
    def save_cache(self, suchwort, res):
        dic = {}
        if exists(config.cache_file):
            dic = pickle.load(file(config.cache_file, "r",-1))
        dic[suchwort] = res
        pickle.dump(dic, file(config.cache_file, "w"),-1)   # Schreibt die DB
    
    def search_cache(self, anfrage):
        """
        Diese Funktion sorgt für einen Suchcache. Der Suchcache
        besteht aus einem pickle-Dic
        
        {SUCHANFRAGE:LISTE_DER_RESULTATE, [...]}
        """
        res = []
        if exists(config.cache_file):
            dic = pickle.load(file(config.cache_file, "r",-1))
            try:
                res = dic[anfrage]
            except KeyError:
                pass
        return(res)
        
    def search(self, anfrage):
        """
        Die Suchfunktion. Diese Funktion kann eigentlich für jedes
        beliebige Programm benutzt werden, welches eine Suchfunktion
        für die Festplatte braucht
        """
        anfrage = anfrage.rstrip()
        anfrage = re.compile(anfrage, re.IGNORECASE)
        
        if self.typ == "index":
            res = self.search_cache(anfrage)
            
            if res != []:
                return res
                
            self.backend.opendb()
            res = self.backend.search(anfrage)
            self.save_cache(anfrage, res)
         
        else:
            rt = rt_searcher()
            res = rt.search(config.root_directory,anfrage)
         
        return(res)
        
#        res = []
#        # Hier wird die Anfrage bearbeitet!
#        files = self.files       # -| Speed
#        keywords = self.keywords # -| Hack
#        speed_len = len          # -|
#        filecount = 0
#        for e in keywords:
#            for i in e:
#                if speed_len(anfrage.findall(i)) >= 1:
#                    hit = files[filecount]
#                    res.append(hit)
#            filecount += 1
#        return res

    def search_xml(self, req):
        """
        Diese Funktion gibt die Suche in XML aus
        praktisch für das kommende Webinterface
        """
        # \todo Echtes XML (DOM oder SAX)
        res = u"""<?xml version="1.0"?>
 <?xml-stylesheet type="text/xsl" href="xml_result.xsl"?>
<result>\n"""
        for i in self.search(req):
            res += unicode ("\t<entry mimetyp='"+str(mimetypes.guess_type(i)[0])+"'>%s</entry>\n" % i, errors = "ignore")
        res += u"</result>"
        return res

