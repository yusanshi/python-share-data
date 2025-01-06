from multiprocessing import Lock, Manager, Process

import numpy as np


def worker_fn():
    with lock:
        # Note: d['numpy'][5000:] -= 1 not works
        # instead, we need to re-assign the key to propagate the changes.
        # refer: https://docs.python.org/3/library/multiprocessing.html#proxy-objects
        temp = d['numpy']
        temp[5000:] -= 1
        d['numpy'] = temp
        d['num'] += 1


if __name__ == '__main__':
    lock = Lock()
    manager = Manager()
    d = manager.dict()
    d['key'] = 'value'
    d['numpy'] = np.ones(shape=(10000, 100))
    d['num'] = 0

    workers = []
    for _ in range(8):
        workers.append(Process(target=worker_fn))
    for x in workers:
        x.start()
    for x in workers:
        x.join()

    print(d)
