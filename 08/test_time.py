import time
from classes import A_init, B_init, C_init
from classes import A_change, B_change, C_change


if __name__ == '__main__':

    n = 100_000
    start_time = time.time()
    print('Class init:')
    A_init(n)
    print("Time taken by A: ", time.time() - start_time)

    start_time = time.time()
    B_init(n)
    print("Time taken by B: ", time.time() - start_time)

    start_time = time.time()
    C_init(n)
    print("Time taken by C: ", time.time() - start_time)
    print('Read and write attr:')
    # Измеряем время чтения/изменения атрибутов
    start_time = time.time()
    A_change(n)
    print("Time taken by A: ", time.time() - start_time)

    start_time = time.time()
    B_change(n)
    print("Time taken by B: ", time.time() - start_time)

    start_time = time.time()
    C_change(n)
    print("Time taken by C: ", time.time() - start_time)
