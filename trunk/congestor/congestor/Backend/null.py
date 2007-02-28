class Cache:
    def __init__(self, options):
        self.__options = options
        self.__storage = options["storage"]

    def could_be(self, query):
        return True
