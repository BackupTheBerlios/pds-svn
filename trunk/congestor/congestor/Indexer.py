# -*- coding:utf8


from Watcher import Watcher

from Backend import Cache, Storage

from os import listdir, path
from os.path import join, isdir, islink
from re import compile

## Nur ein Indexer pro "Namensraum", also entweder ~1000 Dateien oder ein .congestor
#  Verzeichnis
def getSubdirs(d):
    return [
            join(d, i)
            for i in listdir(d)
            if isdir(join(d, i)) and not islink(join(d, i))
            if not i.startswith(".")
           ]

def generateSubindexers(options = {}):
    """Generiert Unterindexer, wenn nötig

    (vorerst immer dann, wenn eine .congestor Datei da ist)
    options ist ein Dictionary mit den geerbten Daten, die aber in der
    .congestor-Datei überschrieben werden können. Eine leere Datei erzwingt
    einfach einen neuen Indexer.
    (Diese Implementierung tut das noch nicht, sie ist stupide!)
    """
    ## \todo Das muss mit dem ersten Indexer-Durchlauf (bzw. dem Watcher
    #        Konstruktor verbunden werden!
    res = {}
    for i in getSubdirs(options["root_directory"]):
        print i
        try:
            options["root_directory"] = i
            res[i] = Indexer(options)
        except OSError:
            pass
    return res

## \todo Handler
## \todo Prioritäten (die die Häufigkeit des refresh-Aufrufs bestimmen)
##       + "Watcher-Overflows" (zu viele Events für einen Watcher)
##          (funktioniert nicht bei mtime)
class Indexer:
    """Indexer-Basisklasse

    Diese Klasse verwaltet die gesammelten Informationen und die Indexer
    für im Dateibaum weiter unten liegende Verzeichnisse und stellt sie
    zur Verfügung."""
    def __init__(self, options):
        """Konstruktor

        options ist ein dictionary, das bisher nur die Parameter
        root_directory und main_priority gesetzt haben braucht. Das
        Verhalten für refresh gehört aber ebenfalls hier hinein."""
        self.__sub_indexers = generateSubindexers(options)
        self.__storage = Storage(options)
        options["cache"]["storage"] = self.__storage
        self.__cache = Cache(options) # self.__storage, self.__sub_indexers)
        options["watcher"]["root_directory"] = options["root_directory"]
        self.__watcher = Watcher(options)

    def __iter__(self):
        """Liefert einen Iterator auf die Sub-Indexer zurück."""
        return iter(self.__sub_indexers)

    def __cmp__(self, other):
        """Vergleichsfunktion, um das Sortieren zu vereinfachen"""
        return cmp(self.__priority, other.__priority)

    def refresh(self):
        res = self.__watcher.collect()
        self.__watcher.reset()

    def could_be(self, query):
        """Unscharfe Suchfunktion

        Diese Funktion soll anhand der Parameter überprüfen, ob eine genaue 
        Übereinstimmung überhaupt möglich ist (ohne die REs zu benutzen).
        Das ganze muss per Rekursion geschehen, um sinnvoll zu sein!
        Die Zwischenergebnisse müssen gecached werden, damit sie in der
        eigentlichen Suche wiederverwendet werden können."""
        return self.__cache.could_be(query)

    def find(self, query):
        return self.__cache.find(query)

    def __refresh_files(filelist):
        """Aktualisierungsfunktion für Dateien

        Aktualisiert alle Dateien in files. files ist ein Dictionary, das
        den Dateinamen (oder die Cachenummer) und die Änderungsart enthält."""
        self.__cache.refresh(filelist)
        for i in filelist:
            self.__handle (i)

    def __refresh_dirs(dirlist):
        """Aktualisierungsfunktion für Verzeichnisse"""
        for i in dirlist["deleted"]:
            del self.__subindexer[i]
        for i in dirlist["created"]:
            options = self.options
            options["root_directory"] = join (self.root_directory, i)
            self.__sub_indexers.append(Indexer(options))
        for i in dirlist["changed"]:
            self.__sub_indexers[i].refresh()

    def __handle(file):
        from mimetypes import guess_type
        type = guess_type(file)[0]
        if type in handler.keys():
            ## Tupel aus Standardelementen und dem Zusatz (ansonsten None)
            self.__storage.replace (file, (mtime, mod, handler[type]))
        else:
            self.__storage.replace (file, (mtime, mod, None))
