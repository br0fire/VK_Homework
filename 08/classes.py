import weakref


class A:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class B:
    __slots__ = ['x', 'y']

    def __init__(self, x, y):
        self.x = x
        self.y = y


class C:
    def __init__(self, x, y):
        self.x = weakref.ref(x)
        self.y = weakref.ref(y)


class FooList(list):
    pass


def A_init(n):
    for i in range(n):
        a = A(FooList([10_000]), FooList([20_000]))


def B_init(n):
    for i in range(n):
        b = B(FooList([10_000]), FooList([20_000]))


def C_init(n):
    for i in range(n):
        c = C(FooList([10_000]), FooList([20_000]))


def A_change(n):
    a = A(FooList([10_000]), FooList([20_000]))
    for i in range(n):
        a.x = FooList([1])
        a.y += FooList([1])


def B_change(n):
    b = B(FooList([10_000]), FooList([20_000]))
    for i in range(n):
        b.x = FooList([1])
        b.y += FooList([1])


def C_change(n):
    c = C(FooList([10_000]), FooList([20_000]))
    for i in range(n):
        x = c.x()
        y = c.y()
        if x is not None:
            x = FooList([1])
        if y is not None:
            y += FooList([1])
