
from util import PriorityQueue as queue

import config

from Indexer import Indexer

class Daemon:
    def __init__(self):
        # \todo Prioritäten
        self.indexer = queue([ Indexer(i) for i in config.roots ], Indexer.priority)

    def poke(self):
        self.indexer.start(config.interval)
        self.indexer.top.start(config.interval)
        self.indexer.push(self.indexer.pop())

