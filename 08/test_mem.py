from memory_profiler import profile
from classes import A_init, B_init, C_init
from classes import A_change, B_change, C_change


if __name__ == '__main__':

    n = 50_000
    A_arr = profile(A_init)(n)

    B_arr = profile(B_init)(n)

    C_arr = profile(C_init)(n)

    profile(A_change)(A_arr)

    profile(B_change)(B_arr)

    profile(C_change)(C_arr)
