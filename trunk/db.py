#! /usr/bin/python
# -*- coding: utf-8 -*-

# SQLite Zugang für PythonDesktopSearch

import sqlite, os, lyp

class pydsdb:
    def __init__(self):
        foo = 0
        if os.path.exists("index.db") != 1:
            foo = 1
        self.con = sqlite.connect('index.db')
        self.cur = self.con.cursor()
        if foo == 1:
            # Erstellt die Tabelle
            self.cur.execute('CREATE TABLE pds(file VARCHAR(100), keywords VARCHAR(50))')
            self.do()
    def add(self, filename, keywords):
        # Fügt etwas hinzu
        self.cur.execute("INSERT INTO pds(file, keywords) VALUES ('"+filename+"', '"+keywords+"')")
    def showall(self):
        self.cur.execute("SELECT * FROM pds")
        return(self.cur.fetchall())
    def sql(self, befehl, do = 1):
        self.cur.execute(befehl)
        if do == 1:
            self.do()
    def do(self):
        self.con.commit()
        
if __name__ == "__main__":
    # DB
    dbuser = pydsdb()
    while 1:
        try:
            dbuser.sql(raw_input("sql ?> "))
        except:
            lyp.cout(error)
    dbuser.showall()
