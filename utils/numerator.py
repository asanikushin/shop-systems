class Numerator:
    def __init__(self, start=0):
        self._cur = start

    def __next__(self):
        out = self._cur
        self._cur += 1
        return out

    next = __next__
