import cProfile
import pstats


class Profiler:
    def __init__(self, func):
        self.func = func
        self.stats = None

    def __call__(self, *args, **kwargs):
        if self.stats is None:
            self.stats = cProfile.Profile()

        self.stats.enable()
        result = self.func(*args, **kwargs)
        self.stats.disable()
        return result

    def print_stat(self):
        if self.stats is None:
            print("No statistics available.")
        else:
            stats = pstats.Stats(self.stats)
            stats.strip_dirs()
            stats.sort_stats("cumulative")
            stats.print_stats()


@Profiler
def add(a, b):
    return a + b


@Profiler
def sub(a, b):
    return a - b


if __name__ == '__main__':
    add(1, 2)
    add(4, 5)
    sub(4, 5)
    add.print_stat()
    sub.print_stat()
