#! /usr/bin/python
# -*- coding: utf-8 -*-

import re

mime_type = "text/html"

def keywords(datei):
    """
    Parst Keywords für die PythonDesktopSearch aus einer
    einfachen HTML Text Datei
    MIME-Type: text/html
    """
    keys = []
    f = open(datei, "r")
    search = ['<meta name="keywords" content="', '<meta name="description" content="']
    for i in f:
        i = i.lower()
        if i.find(search[0]) > -1:
            i = i.replace(search[0],"").replace(">","").replace("/","").replace('"',"").replace("\n","").replace("\r","")
            i = i.split(", ")
            keys.extend(i)
        elif i.find(search[1]) > -1:
            i = i.replace(search[1],"").replace(">","").replace("/","").replace('"',"").replace("\n","").replace("\r","")
            i = i.split(", ")
            keys.extend(i)
    f.close()
    return(keys)
    
if __name__ == "__main__":
    print keywords("mime_testfiles/index.htm")
