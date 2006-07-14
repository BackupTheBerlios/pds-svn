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
from pds import *

import config

def command():
    pds = Finder()
    anfrage = " "
    while 1:
#        if anfrage != "":
#            cout("\nIhre Suchanfrage (in RE)? ('/quit' zum Beenden)")
        anfrage = raw_input("?> ")
        if anfrage == "/quit":
            break
        elif anfrage == "":
            pass
        else:
            res = pds.search(anfrage)
            cout (str(len(res)) + " Treffer:")
            for i in res:
                cout(do_color(i, anfrage))
    sys.exit (0)

def docolor(req):
    for i in pds.search(req):
        cout(do_color(i, req))

def doxml(req):
    cout (pds.search_xml(req))

def doplain(req):
    for i in pds.search(req):
        cout(i)

class set_output:
    def __init__(self, f):
        self.f = f
    def __call__(self):
        global output
        output = self.f

if __name__ == "__main__":
    output = docolor

    long_options = {
            "command" : command,
            "nocolor" : set_output (doplain),
            "xml" : set_output (doxml)
            }

    short_options = {
            "c" : "command",
            "C" : "nocolor",
            "x" : "xml"
            }

    description = {
            "command" : "Startet die Kommandozeile",
            "nocolor" : "Farbausgabe",
            "xml" : "XML Daten ausgeben"
            }

    def usage():
        done = []
        cout ("\n[%s] Python Desktop Search v.%s\n" % (sys.argv[0], config.version))
        for i in short_options:
            j = short_options[i]
            cout ("--%s [-%s]\t\t%s" % (j, i, description[j]))
            done.append (j)
        for j in long_options:
            if not j in done:
                cout ("--%s\t\t%s" % (j, description[j]))
        cout("\n")
        sys.exit (0)

    def parse_long_command(s):
        if s == "help":
            usage()
        if long_options.has_key(s):
            long_options[s]()
        else:
            usage()

    def parse_short_command(s):
        if 'h' in s:
            usage()
        for i in short_options:
            j = short_options[i]
            if i in s:
                long_options[j]()

    argv = sys.argv[1:]

    if len(argv) == 0:
        usage()
    
    req = ""

    for i in argv:
        if not len(req):
            if i.startswith("--"):
                parse_long_command(i[2:])
            elif i.startswith("-"):
                parse_short_command(i[1:])
            else:
                req += i
        else:
            req = req + " " + i
    
    pds = Finder()
    output(req)

