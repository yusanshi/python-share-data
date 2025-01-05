from multiprocessing import Process

import numpy as np
# pip install UltraDict
from UltraDict import UltraDict


def worker_fn():
    with ultra.lock:
        # Note: ultra['numpy'][5000:] -= 1 not works
        # TODO: an accurate explanation of why the following works
        temp = ultra['numpy']
        temp[5000:] -= 1
        ultra['numpy'] = temp


if __name__ == '__main__':
    ultra = UltraDict()
    ultra['key'] = 'value'
    ultra['numpy'] = np.ones(shape=(10000, 100))

    workers = []
    for _ in range(8):
        workers.append(Process(target=worker_fn))
    for x in workers:
        x.start()
    for x in workers:
        x.join()

    print(ultra)
