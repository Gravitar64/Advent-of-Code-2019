from collections import deque
import time

time_start = time.perf_counter()


with open('tag16.txt') as f:
  puzzle_input = f.readline()

signal = [int(x) for x in puzzle_input]*10_000
offset = int(puzzle_input[:7])
signal_len = len(signal)

for i in range(100):
  partial_sum = sum([signal[j] for j in range(offset, signal_len)])
  for j in range(offset, signal_len):
    t = partial_sum
    partial_sum -= signal[j]
    signal[j] = t % 10 if t >= 0 else (-t) % 10
  
lösung = "".join(map(str, signal[offset:offset+8]))
print(f'Lösung = {lösung} in {time.perf_counter()-time_start}')
