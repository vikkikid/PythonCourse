import os
import time
from threading import Thread
from multiprocessing import Process


def fib(n):
    '''
    first n fib numbers from hw1
    '''
    assert n >= 0
    f0, f1 = 0, 1
    first_n = [f0, f1]
    for _ in range(n - 2):
        f0, f1 = f1, f0 + f1
        first_n.append(f1)
    return first_n[:n]


if __name__ == '__main__':
    path = 'artifacts'
    easy = path + '/easy'
    os.makedirs(easy, exist_ok=True)
  
    n = 10**5
    k = 10

    # 1 - sync
    t0 = time.time()
    for _ in range(k):
        fib(n)
    sync = time.time() - t0

    # 2 - process
    t0 = time.time()
    processes = [Process(target=fib, args=(n,)) for _ in range(k)]
    for i in processes:
        i.start()
    for i in processes:
        i.join()
    pr = time.time() - t0
    
    # 3 - thread
    t0 = time.time()
    threads = [Thread(target=fib, args=(n,)) for _ in range(k)]
    for j in threads:
        j.start()
    for j in threads:
        j.join()
    thr = time.time() - t0

    # save results
    with open(f"{easy}/one.txt", "w") as file:
        file.write(f"sync time is {sync.__str__()}")
        file.write(f"\nprocess time is {pr.__str__()}")
        file.write(f"\nthreads time is {thr.__str__()}\n")
