from memory_profiler import profile
from classes import A_init, B_init, C_init
from classes import A_change, B_change, C_change



if __name__ == '__main__':

    n = 100_000
    profile(A_init)(n)

    profile(B_init)(n)

    profile(C_init)(n)

    profile(A_change)(n)

    profile(B_change)(n)

    profile(C_change)(n)
