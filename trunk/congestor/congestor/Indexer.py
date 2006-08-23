import config

from os import listdir, path
from os.path import join, isdir, islink

# \depr Ein Indexer Objekt pro Verzeichnis
# Nur ein Indexer pro "Namensraum", also entweder ~1000 Dateien oder ein .brian
# Verzeichnis

def getSubdirs(d):
    return [
            join(d, i)
            for i in listdir(d)
            if isdir(join(d, i)) and not islink(join(d, i))
            if not i.startswith(".")
           ]

#Argh, Opts wird hier verändert!
def generateSubindexers (Opts):
    asdf = type ('', (), (Opts._dict)) ()
    res = []
    for i in getSubdirs(Opts.root_directory):
        print i
        asdf.root_directory = i
        try:
            res.append(Indexer(asdf))
        except OSError:
            pass
    return res

class Indexer:
    def __init__(self, directory):
        self._sub_indexers = PriorityQueue(generateSubindexers(Opts))
        self._main_priority = Opts.main_priority
        self._priority = self._main_priority
        self._root_directory = directory
        self._cache = Cache (self._root_directory)

    def __cmp__(self, other):
        return cmp(self._priority, other._priority)

    def refresh(self):
        self._priority -= (self._main_priority / 10) # Dynamischer (nach delta-mtime)
        if askmtime() > self._mtimе:
            if self._subindexers:
                for i in self._subindexers:
                    i.refresh()
            for i in self._files:
                i = refreshFile(i)
