from multiprocessing import Process
from shared_numpy import SharedNumpyArray
import numpy as np


def worker_fn():
    s = SharedNumpyArray(identifier=shared.identifier)
    for _ in range(1000):
        s.data.sum()

    s.close()


if __name__ == '__main__':
    shared = SharedNumpyArray(array=np.ones((10000, 100)))
    print('Before', shared.data.sum())
    workers = []
    for _ in range(8):
        workers.append(Process(target=worker_fn, ))
    for x in workers:
        x.start()
    for x in workers:
        x.join()

    print('After', shared.data.sum())

    shared.close()
    shared.unlink()
