import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
import numpy as np


class Snake(object):
    def __init__(self, points, symbol="#"):
        self.key = None
        self.score = 0
        self.points = points
        self.symbol = symbol
        self.dead = False

    @property
    def length(self):
        if self.dead:
            return self.score
        else:
            return self.points.shape[0]

    def killme(self):
        self.score = self.length
        self.dead = True

    def get_move(self):
        self.key = KEY_RIGHT

    def __str__(self):
        s = "Snake ({}) {}".format(self.symbol, self.points)
        return s


# if __name__ == "__main__":
#     s1 = Snake()
