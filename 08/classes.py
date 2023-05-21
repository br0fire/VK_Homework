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
    class_arr = [A(FooList([10_000]), FooList([20_000])) for i in range(n)]
    return class_arr


def B_init(n):
    class_arr = [B(FooList([10_000]), FooList([20_000])) for i in range(n)]
    return class_arr


def C_init(n):
    class_arr = [C(FooList([10_000]), FooList([20_000])) for i in range(n)]
    return class_arr


def A_change(arr):
    for i in range(len(arr)):
        arr[i].x = FooList([1000]*5)
        arr[i].y += FooList([1000]*5)


def B_change(arr):
    for i in range(len(arr)):
        arr[i].x = FooList([1000]*5)
        arr[i].y += FooList([1000]*5)


def C_change(arr):
    for i in range(len(arr)):
        x = arr[i].x()
        y = arr[i].y()
        if x is not None:
            x = FooList([1000]*5)
        if y is not None:
            y += FooList([1000]*5)
