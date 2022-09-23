import random


class RandomModel:
    def __init__(self, n=4):
        self.n = n
        self.k = 0

    @property
    def x(self):
        self.k += 1
        return [random.randint(0, 127) for i in range(self.n)]
