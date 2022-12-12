# Python: sharing data between processes

Some examples of how to share data (especially tensors or arrays in deep learning tasks) between processes in Python.

Tips:
- Use `ultradict.py` for sharing small data.
- Use `shm_*.py` or `torch_*.py` for sharing large tensors or arrays.

Note: for Linux only.

## Benchmark

### read

```
hyperfine "python torch_read.py" "python torch_cuda_read.py" "python shm_read.py"
```
```
Benchmark 1: python torch_read.py
  Time (mean _ _):      3.207 s _  0.135 s    [User: 3.060 s, System: 3.315 s]
  Range (min _ max):    3.032 s _  3.463 s    10 runs
 
Benchmark 2: python torch_cuda_read.py
  Time (mean _ _):      7.988 s _  0.226 s    [User: 3.607 s, System: 4.329 s]
  Range (min _ max):    7.601 s _  8.276 s    10 runs
 
Benchmark 3: python shm_read.py
  Time (mean _ _):     626.2 ms _  29.8 ms    [User: 3538.7 ms, System: 2021.8 ms]
  Range (min _ max):   564.4 ms _ 671.4 ms    10 runs
 
Summary
  'python shm_read.py' ran
    5.12 _ 0.33 times faster than 'python torch_read.py'
   12.76 _ 0.71 times faster than 'python torch_cuda_read.py'
```

### write
```
hyperfine "python torch_write.py" "python torch_cuda_write.py" "python shm_write.py"
```
```
Benchmark 1: python torch_write.py
  Time (mean _ _):      3.269 s _  0.136 s    [User: 2.968 s, System: 3.400 s]
  Range (min _ max):    3.119 s _  3.541 s    10 runs
 
Benchmark 2: python torch_cuda_write.py
  Time (mean _ _):      7.685 s _  0.197 s    [User: 3.436 s, System: 4.197 s]
  Range (min _ max):    7.344 s _  8.027 s    10 runs
 
Benchmark 3: python shm_write.py
  Time (mean _ _):      3.034 s _  0.059 s    [User: 3.538 s, System: 2.139 s]
  Range (min _ max):    2.920 s _  3.099 s    10 runs
 
Summary
  'python shm_write.py' ran
    1.08 _ 0.05 times faster than 'python torch_write.py'
    2.53 _ 0.08 times faster than 'python torch_cuda_write.py'
```

## TODO

```bash
$ grep "TODO" *.py
torch_cuda_write.py:# TODO: why don't need the lock
torch_cuda_write.py:# TODO: why don't need the share_memory_
torch_cuda_write.py:# TODO: wrong results if the shared tensor is too big, e.g., size=(10000, 1000), even with a lock
torch_read.py:        # data.sum()  # TODO: no lock -> low speed, why?
ultradict.py:        # TODO: an accurate explanation of why the following works
```
