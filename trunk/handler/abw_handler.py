#! /usr/bin/python
# -*- coding: utf-8 -*-

from xml.dom import minidom

mime_type = "application/x-abiword"

def keywords(datei):
    """
    Parst Keywords für die PythonDesktopSearch aus einer
    AbiWord XML Datei
    MIME-Type: application/x-abiword
    """
    keys = []
    tmp = minidom.parse(datei)
    for i in [i for i in tmp.getElementsByTagName("p")
if i.attributes["style"].value == "Heading 1" or \
i.attributes["style"].value == "Heading 2" or \
i.attributes["style"].value == "Heading 3" or \
i.attributes["style"].value == "Heading 4"]:
        try:
            keys.append(str(i.firstChild.firstChild.data))
        except:
            pass
    del tmp
    return(keys)

