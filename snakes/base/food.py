
class Food(object):
    def __init__(self, symbol="*"):
        self.symbol = symbol
        self.nfood = 0

    @property
    def length(self):
        return self.nfood

    def __str__(self):
        s = "Food ({}) {}".format(self.symbol, self.nfood)
        return s