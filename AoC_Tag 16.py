from collections import deque
import time

time_start = time.perf_counter()

standard_pattern = deque([0, 1, 0, -1])
with open('tag16.txt') as f:
  puzzle_input = f.readline()

input_signal = [int(x) for x in puzzle_input]

def generate_pattern(länge_input):
  patterns = {}
  for phase in range(1,länge_input+1):
    pattern = deque()
    for zahl in standard_pattern:
      for i in range(phase):
        pattern.append(zahl)
    pattern.rotate(-1)
    patterns[phase] = pattern    
  return patterns

def fft(signal):
  fft = []
  for phase in range(len(signal)):
    summe = 0
    pattern = patterns[phase+1].copy()
    for i in range(len(signal)):
      summe += signal[i] * pattern[0]
      pattern.rotate(-1)
    last_digit = abs(summe) % 10
    fft.append(last_digit)
  return fft

patterns = generate_pattern(len(input_signal))
for _ in range(100):
  input_signal = fft(input_signal)

print(f'Lösung = {"".join(map(str,input_signal[:8]))} in {time.perf_counter()-time_start}')
