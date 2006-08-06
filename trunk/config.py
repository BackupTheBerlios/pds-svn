# -*- coding: utf-8 -*-
#
# Config File für die PythonDesktopSearch

version = "0.2.1"   # Sinnlos dies zu ändern
                     
color = 1           # Standart Highlighting von Treffer

such_cache = 1      # Anlegen eines Such Cache

threads = 0       # Anzahl maximal laufender Threads 0 = keine Threads
                  # Das Threading ist noch in der AlphaPhase!!

blacklist = ["\.pds"]                 # Dateien, auf die dieses Pattern passt
                                      # werden nicht indexiert

whitelist =  []                       # Hebt die Vorgaben der Blacklist auf

cache_path = "/var/cache"
tmp_path = "/tmp/"

root_directory = "/"

backend = "pickle"  # Gibt an welches Backend benutzt werden soll
                    # pickle, sqlite
# Wenn sqlite & pickle wird es automatisch in dem cache_path gespeichert
# Bei mysql sind die untigen Daten anzugeben

# MYSQL IST NOCH NICHT EINGEBAUT!!
# Wenn mysql:
mysql = {"user":"IHR_USERNAME", "passwd":"IHR_PASSWORT", 
        "db":"DIE_DB", "table":"pds"}
# / mysql

# Ab hier bitte nichts mehr ändern!
# Import
from os.path import join
import re
# / Import

# Erstelle Black- & White-list
blacklist = [re.compile(i) for i in blacklist]
whitelist = [re.compile(i) for i in whitelist]
# / ende

del re # |- Myll

index_file = join (cache_path, "index.pds")
cache_file = join (tmp_path, "search_cache.pds")

# blacklist = ["etc", "usr", "man", "dev", "initrd", "opt", "proc", "root", "sbin", "srv", "sys"]
