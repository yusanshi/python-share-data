# Python: sharing data between processes

## Benchmark

### read


```
hyperfine "python torch_read.py" "python shm_read.py"
```
```
Benchmark 1: python torch_read.py
  Time (mean ± σ):      2.834 s ±  0.314 s    [User: 1.353 s, System: 1.134 s]
  Range (min … max):    2.494 s …  3.608 s    10 runs
 
Benchmark 2: python shm_read.py
  Time (mean ± σ):     918.2 ms ±  81.1 ms    [User: 6247.8 ms, System: 997.7 ms]
  Range (min … max):   812.9 ms … 1075.2 ms    10 runs
 
Summary
  'python shm_read.py' ran
    3.09 ± 0.44 times faster than 'python torch_read.py'
```

### write
```
hyperfine "python torch_write.py" "python shm_write.py"
```
```
Benchmark 1: python torch_write.py
  Time (mean ± σ):      3.201 s ±  0.499 s    [User: 1.447 s, System: 1.004 s]
  Range (min … max):    2.605 s …  4.045 s    10 runs
 
Benchmark 2: python shm_write.py
  Time (mean ± σ):      8.641 s ±  0.758 s    [User: 8.760 s, System: 1.188 s]
  Range (min … max):    7.641 s …  9.832 s    10 runs
 
Summary
  'python torch_write.py' ran
    2.70 ± 0.48 times faster than 'python shm_write.py'
```

## TODO

- Pytorch: read mode, no lock -> low speed, why?
- Pytorch: memory usage increase with numbers of processes, although less than the plain pickling-and-unpicking, with a small file in /dev/shm, what happens?

