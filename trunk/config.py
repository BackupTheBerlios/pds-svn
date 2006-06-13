#coding: utf-8
#
# Config File für die PythonDesktopSearch

version = "0.1.1"    # Es ist ziemlich unnütz diese Variable zu ändern^^
                     # Also mach es nicht! ;)

commit = 1000000     # Nach wie viel Dateien ein commit?
                     # Je hoher desto schneller desto unsicherer

show_page = False    # Zeigt die Box mit "Seite X von X"
                     # wenn false macht er auch keine Pause
                     
color = False        # Wenn True werden die Treffer Rot eingefärbt

treffer_page = 50    # Wie viele Treffer sollen auf einer Page angezeigt werden?

tage = 7             # Alle wie viel Tage soll ein neues Index erstellt werden

blacklist = []       # index all

direct_new_cache = 1 # Erstellt nach dem Index Prozess eine neue Cache Datei


# Bausteine:
# Blacklist mit Sachen die man normalerweise nicht braucht^^
#blacklist = ["etc", "usr", "man", "dev", "initrd", "opt", "proc", "root", "sbin", "srv", "sys"]
