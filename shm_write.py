from multiprocessing import Lock, Process

import numpy as np

from shared_numpy import SharedNumpyArray


def increase():
    s = SharedNumpyArray(identifier=shared.identifier)
    for _ in range(1000):
        with lock:
            s.data += 1

    s.close()


def decrease():
    s = SharedNumpyArray(identifier=shared.identifier)
    for _ in range(1000):
        with lock:
            s.data -= 1

    s.close()


if __name__ == '__main__':
    shared = SharedNumpyArray(array=np.ones((10000, 100)))
    print('Before', shared.data.sum())
    # Note: don't need the lock if different workers always write to different locations.
    # e.g., worker 0 writes to row 0, 4, 8, ..., workers 1 writes to row 1, 5, 9, ...
    lock = Lock()
    workers = []
    for _ in range(4):
        workers.append(Process(target=increase))
        workers.append(Process(target=decrease))
    for x in workers:
        x.start()
    for x in workers:
        x.join()

    print('After', shared.data.sum())

    shared.close()
    shared.unlink()
