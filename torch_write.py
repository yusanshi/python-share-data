from torch.multiprocessing import Process, set_start_method, Lock
import torch


def increase(data, lock):
    for _ in range(1000):
        with lock:
            data -= 1


def decrease(data, lock):
    for _ in range(1000):
        with lock:
            data += 1


if __name__ == '__main__':
    set_start_method('forkserver')  # or 'spawn'

    data = torch.ones(size=(10000, 100))
    print('Before', data.sum())

    lock = Lock()
    workers = []
    for _ in range(4):
        workers.append(Process(target=increase, args=(data, lock)))
        workers.append(Process(target=decrease, args=(data, lock)))
    for x in workers:
        x.start()
    for x in workers:
        x.join()

    print('After', data.sum())
