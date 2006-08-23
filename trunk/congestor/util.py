
def less(x, y):
    if x < y:
        return -1
    elif x == y:
        return 0
    elif x > y:
        return 1

def push_heap(mylist, val, comp = less, length = 0):
    pass

def make_heap(mylist, comp = less):
    pass

def adjust_heap(mylist, comp = less):
    pass

def pop_heap(mylist, comp = less):
    pass

class PriorityQueue:
    def __init__(self, my_list = [], comp = less):
        self._comp = comp
        self._list = my_list
        self._list.sort(cmp = comp)

    def top(self):
        return self._list[len(self._list)-1]

    def pop(self):
        return self._list.pop()

    def push(self, el):
        self._list.append(el)
        self._list.sort(cmp = self._comp)

    def _my_comp(self, x, y):
        return self._comp(x, y)
