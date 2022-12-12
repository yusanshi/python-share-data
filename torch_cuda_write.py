from torch.multiprocessing import Process, set_start_method
import torch

# TODO: why don't need the lock
# TODO: why don't need the share_memory_
# TODO: wrong results if the shared tensor is too big, e.g., size=(10000, 1000), even with a lock


def increase(data):
    for _ in range(1000):
        data -= 1


def decrease(data):
    for _ in range(1000):
        data += 1


if __name__ == '__main__':
    set_start_method('forkserver')  # or 'spawn'

    data = torch.ones(size=(10000, 100)).cuda()
    print('Before', data.sum())

    workers = []
    for _ in range(4):
        workers.append(Process(target=increase, args=(data, )))
        workers.append(Process(target=decrease, args=(data, )))
    for x in workers:
        x.start()
    for x in workers:
        x.join()

    print('After', data.sum())
