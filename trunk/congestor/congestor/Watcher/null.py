class Watcher:
    def __init__(self, options):
        self.__root = options["root_directory"]
        self.__objects = getObjects(self.__root)
    def collect(self):
        return self.__objects
    def reset(self):
        pass
