from torch.multiprocessing import Process, set_start_method
import torch


def worker_fn(data):
    for _ in range(1000):
        data.sum()


if __name__ == '__main__':
    set_start_method('forkserver')  # or 'spawn'

    data = torch.ones(size=(10000, 100)).cuda()
    print('Before', data.sum())

    workers = []
    for _ in range(8):
        workers.append(Process(target=worker_fn, args=(data, )))
    for x in workers:
        x.start()
    for x in workers:
        x.join()

    print('After', data.sum())
