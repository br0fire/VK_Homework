from itertools import zip_longest


class CustomList(list):
    def __init__(self, lst):
        super().__init__(lst)

    def __add__(self, other):
        res = zip_longest(self, other, fillvalue=0)
        return CustomList(map(lambda x: x[0] + x[1], res))

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        res = zip_longest(self, other, fillvalue=0)
        return CustomList(map(lambda x: x[0] - x[1], res))

    def __rsub__(self, other):
        res = zip_longest(self, other, fillvalue=0)
        return CustomList(map(lambda x: x[1] - x[0], res))

    def __lt__(self, other):
        return sum(self) < sum(other)

    def __le__(self, other):
        return sum(self) <= sum(other)

    def __gt__(self, other):
        return sum(self) > sum(other)

    def __ge__(self, other):
        return sum(self) >= sum(other)

    def __eq__(self, other):
        return sum(self) == sum(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return super().__str__() + ", sum=" + str(sum(self))
