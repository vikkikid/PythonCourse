import os
import time
import codecs
from datetime import datetime
from threading import Thread
from multiprocessing import Process, Pipe, Queue
from multiprocessing.connection import Connection


def fib(n):
    '''
    first n fib numbers from hw1, for easy task
    '''
    assert n >= 0
    f0, f1 = 0, 1
    first_n = [f0, f1]
    for _ in range(n - 2):
        f0, f1 = f1, f0 + f1
        first_n.append(f1)
    return first_n[:n]


def a_w(in_q: Queue, out_p: Connection):
    '''
    A worker, for hard task
    '''
    while True:
        msg = in_q.get()
        time.sleep(5)
        out_p.send(msg.lower())


def b_w(in_p: Connection, out_p: Connection):
    '''
    B worker, for hard task
    '''
    while True:
        out_p.send(codecs.encode(in_p.recv(), "rot_13"))



if __name__ == '__main__':
    path = 'artifacts'
    easy = path + '/easy'
    hard = path + '/hard'
    os.makedirs(easy, exist_ok=True)
    os.makedirs(hard, exist_ok=True)
 
    # _________
    # easy part
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

    # _________
    # hard part
    main2a = Queue()
    a2b, b2a = Pipe()
    b2main, main2b = Pipe()
    all_msg = []
    Process(target=a_w, args=(main2a, a2b), daemon=True).start()
    Process(target=b_w, args=(b2a, b2main), daemon=True).start()
    
    while True:
        msg = input('>')
        if msg == 'stop':
            break
            
        all_msg.append(f'Recieve. {datetime.now()}: {msg}\n')
        main2a.put(msg)
        msg = main2b.recv()
        all_msg.append(f'Result. {datetime.now()}: {msg}\n')

        with open(f"{hard}/three.txt", "w") as file:
            for i in all_msg:
                file.write(i)
