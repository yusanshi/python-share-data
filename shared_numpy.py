from multiprocessing import shared_memory
import numpy as np


class SharedNumpyArray(shared_memory.SharedMemory):

    def __init__(self, array=None, name=None, shape=None, dtype=None):
        if array is None:
            # attach to the existing shared memory
            # `SharedNumpyArray(name, shape, dtype)`
            assert name is not None
            assert shape is not None
            assert dtype is not None
            super().__init__(name=name, create=False)
            self.data = np.ndarray(shape, dtype=dtype, buffer=self.buf)
        else:
            # create new shared memory
            # `SharedNumpyArray(array)`
            # or `SharedNumpyArray(array, name)`
            assert isinstance(array, np.ndarray)
            assert shape is None
            assert dtype is None
            super().__init__(name=name, create=True, size=array.nbytes)
            self.data = np.ndarray(array.shape,
                                   dtype=array.dtype,
                                   buffer=self.buf)
            self.data[:] = array[:]

    def __repr__(self):
        return super().__repr__() + '\n' + self.data.__repr__()


if __name__ == '__main__':
    a = SharedNumpyArray(array=np.ones((1000, 1000)))
    b = SharedNumpyArray(name=a.name, shape=a.data.shape, dtype=a.data.dtype)

    print(a.data, '\n\n', b.data, '\n\n')
    a.data[:500] += 1

    print(a.data, '\n\n', b.data, '\n\n')
    b.data[500:] -= 1
    print(a.data, '\n\n', b.data, '\n\n')

    a.close()
    b.close()
    a.unlink()
