from multiprocessing import Process, Lock
from shared_numpy import SharedNumpyArray
import numpy as np


def increase():
    s = SharedNumpyArray(identifier=shared.identifier)
    for _ in range(1000):
        with lock:
            s.data -= 1

    s.close()


def decrease():
    s = SharedNumpyArray(identifier=shared.identifier)
    for _ in range(1000):
        with lock:
            s.data += 1

    s.close()


if __name__ == '__main__':
    shared = SharedNumpyArray(array=np.ones((10000, 100)))
    print('Before', shared.data.sum())
    lock = Lock()
    workers = []
    for _ in range(4):
        workers.append(Process(target=increase, ))
        workers.append(Process(target=decrease, ))
    for x in workers:
        x.start()
    for x in workers:
        x.join()

    print('After', shared.data.sum())

    shared.close()
    shared.unlink()
