#! /usr/bin/python
# -*- coding: utf8 -*-
#
# rt_sarch.py is a part of PythonDesktopSearch
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

# Diese Datei sorgt für eine Echtzeit suche
    # Fehlerhaft

import os
import re
import time
import mimetypes
from os.path import join, getsize
import sys
import thread

import handler
from lyp import *
import config

class rt_searcher:
    """
    Echtzeit suche der pyfind
        quasi ein Indexer mit direkter Suche
    """
    def __init__(self):
        self.warteliste = []
        self.threads = 0
        self.res = []
    
    def warteschlange(self, arg, dirname, files):
        self.warteliste.append((arg, dirname, files))
        
    def _thread_scan(self):
        """
        Diese Funktion arbeitet die Warteschlange
        mit einer Anzahl von XXX Threads ab
        """
        while len(self.warteliste) > 0:
            if self.threads <= config.threads:
                self.threads += 1
                thread.start_new_thread(self._makelist, self.warteliste.pop())
                

    def _makelist(self, arg, dirname, files):
        
        if self._check_bw_lists("", dirname):
            for i in files:
                if not self._check_bw_lists(i, dirname):
                    continue
                key = []
                filename = join (dirname, i)
                # \todo Per Timestamp nach Änderung fragen und gegebenfalls Handler
                #       aufrufen
#                if filename in filesback:
#                    break
                filetype = mimetypes.guess_type(i)
                try:
                    key = handler.filetypes[filetype[0]](filename) #öffnet den Handler
                except:
                    pass
                    
                    
                key.append(i)
                
                for e in key:
                    if len(self.anfrage.findall(e)) >= 1:
                        self.res.append(filename)
                        break
                
            self.threads -= 1

    def search(self, searchdir, anfrage):
        self.anfrage = re.compile(anfrage, re.IGNORECASE)
        if config.threads != 0:
            os.path.walk(searchdir, self.warteschlange, "")
            self._thread_scan()
        else:
            os.path.walk(root, self._makelist, "")
        return(res)
        

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
    rt = rt_searcher()
    rt.scan("/home/sigma/", "test")
