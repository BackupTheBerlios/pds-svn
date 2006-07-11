# -*- coding: utf-8 -*-
#
# Config File für die PythonDesktopSearch

version = "0.2_gentoo"
                     
color = 1

blacklist = ["\.pds"]                  # Dateien, auf die dieses Pattern passt
                                       # werden nicht indexiert

whitelist =  []    # Hebt die Vorgaben der Blacklist auf

cache_path = "/var/cache"

root_directory = "/"


# pfad = "/home/sigma/work/pythondesktopsearch" # Installationsort


# Ab hier bitte nichts mehr ändern!
from os.path import join
import re

blacklist = [re.compile(i) for i in blacklist]
whitelist = [re.compile(i) for i in whitelist]

del re

index_file = join (cache_path, "index.pds")

# blacklist = ["etc", "usr", "man", "dev", "initrd", "opt", "proc", "root", "sbin", "srv", "sys"]
