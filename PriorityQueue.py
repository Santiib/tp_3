from Queue import PriorityQueue
class ColaPrioridad(PriorityQueue):

    def __init__(self, maxsize = 0):

        PriorityQueue.__init__(self, maxsize)
        

    def first(self):

        return self.queue[0]
