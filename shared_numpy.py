import base64
import pickle
from multiprocessing.shared_memory import SharedMemory

import numpy as np


class SharedNumpyArray(SharedMemory):

    def __init__(self, *, array=None, identifier=None):
        if array is None:
            # attach to the existing shared memory
            # `SharedNumpyArray(identifier)`
            assert identifier is not None
            name, shape, dtype = self._str2obj(identifier)
            super().__init__(name=name, create=False)
            self.data = np.ndarray(shape, dtype=dtype, buffer=self.buf)
            self.identifier = identifier
        else:
            # create new shared memory
            # `SharedNumpyArray(array)`
            assert isinstance(array, np.ndarray)
            assert identifier is None
            super().__init__(name=None, create=True, size=array.nbytes)
            self.data = np.ndarray(array.shape,
                                   dtype=array.dtype,
                                   buffer=self.buf)
            self.data[:] = array[:]
            self.identifier = self._obj2str(self.name, array.shape,
                                            array.dtype)

    def __repr__(self):
        return super().__repr__() + '\n' + self.data.__repr__()

    @staticmethod
    def _obj2str(*args):
        # return pickle.dumps(args, protocol=0).decode()
        return base64.b64encode(pickle.dumps(args)).decode()

    @staticmethod
    def _str2obj(string):
        # return pickle.loads(string.encode())
        return pickle.loads(base64.b64decode(string.encode()))


if __name__ == '__main__':
    a = SharedNumpyArray(array=np.ones((1000, 1000)))  # create
    b = SharedNumpyArray(identifier=a.identifier)  # attach

    print(a.data, '\n\n', b.data, '\n\n')
    a.data[:500] += 1

    print(a.data, '\n\n', b.data, '\n\n')
    b.data[500:] -= 1
    print(a.data, '\n\n', b.data, '\n\n')

    a.close()
    b.close()
    a.unlink()
