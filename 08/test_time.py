import time
from classes import A_init, B_init, C_init
from classes import A_change, B_change, C_change


if __name__ == '__main__':

    n = 5_000_000
    start_time = time.time()
    print('Class init:')
    A_arr = A_init(n)
    print("Time taken by A: ", time.time() - start_time)

    start_time = time.time()
    B_arr = B_init(n)
    print("Time taken by B: ", time.time() - start_time)

    start_time = time.time()
    C_arr = C_init(n)
    print("Time taken by C: ", time.time() - start_time)
    print('Read and write attr:')
    # Измеряем время чтения/изменения атрибутов
    start_time = time.time()
    A_change(A_arr)
    print("Time taken by A: ", time.time() - start_time)

    start_time = time.time()
    B_change(B_arr)
    print("Time taken by B: ", time.time() - start_time)

    start_time = time.time()
    C_change(C_arr)
    print("Time taken by C: ", time.time() - start_time)
