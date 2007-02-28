from os.path import getmtime

def getObjects (path):
    return []

class Watcher:
    def __init__(self, options):
        self.__root = options["root_directory"]
        self.__objects = {}
        self.reset()
        for i in getObjects(self.__root):
            self.__objects[i] = getmtime(i)
    def collect(self):
        # TODO deleted, modified, created
        return [ i for i,j in self.__objects if getmtime(i) > j ]
    def reset(self):
        # s.o.
        for i in getObjects(self.__root):
            self.__objects[i] = getmtime(i)
