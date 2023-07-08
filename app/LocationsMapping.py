import math


class CarsLocations():
    def __init__(self):
        self.locations = set()

    def add(self, tuple):
        a, b, c, d = tuple

        if len(self.locations) < 1:
            self.locations.add(tuple)
            return

        for index, i in enumerate(self.locations.copy()):
            a1, b1, c1, d1 = i

            if math.fabs(a1 - a) < 30:
                self.locations.remove(i)

            if math.fabs(a1 - a) > 30:
                self.locations.add(tuple)
