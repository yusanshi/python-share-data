import torch
from torch.multiprocessing import Lock, Process, set_start_method


def worker_fn(data, lock):
    for _ in range(1000):
        # data.sum()  # TODO: no lock -> low speed, why?
        with lock:
            data.sum()


if __name__ == '__main__':
    set_start_method('forkserver')  # or 'spawn'

    data = torch.ones(size=(10000, 100))
    print('Before', data.sum())

    lock = Lock()
    workers = []
    for _ in range(8):
        workers.append(Process(target=worker_fn, args=(data, lock)))
    for x in workers:
        x.start()
    for x in workers:
        x.join()

    print('After', data.sum())
