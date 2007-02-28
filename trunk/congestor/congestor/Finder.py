"""
Ueberarbeiten, Finder wird von einer anderen Anwendung angelegt und hat
somit keinen Zugriff auf den laufenden Indexer!
"""

class Finder:
    def __init__(self, indexer):
        self.__indexer = indexer

    def find(self, query):
        """Suchfunktion

        Die Syntax für den string query muss noch festgelegt werden, ist
        aber grundsätzlich eine erweiterte RE (siehe ql)."""
        if type(query) != dict:
            query = self.__parse(query)
        res = []
        for i in self.indexer:
            if i.could_be(query):
                res += i.find(query)
        res += self.indexer.find(query)

    def __parse(query):
        """Parserfunktion

        Parset die Abfrage in query zu einem Dictionary von REs.
        query hat dabei die Form:
            x = .*; y = \ *;"""
        ## \todo Splits überarbeiten, sodass sie escaped werden können und immer
        #        nur eins auch aufgenommen wird. (Wichtig: auch ein Space der Form
        #        \ muss am Ende übersprungen werden).
        res = {}
        l = [ i for i in query.split(';') if i != '' ]
        for i in l:
            a = [ b.strip() for b in i.split ('=') ]
            res[a[0]] = compile(a[1])

