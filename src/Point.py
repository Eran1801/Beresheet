import math


class Point:
    def _init_(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        # distance between
        return math.sqrt((self.x - other.x) * 2 + (self.y - other.y) * 2)
