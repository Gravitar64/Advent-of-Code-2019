from collections import defaultdict
import time
time_start = time.perf_counter()

planeten = defaultdict(list)
with open('tag06.txt') as f:
  for line in f.readlines():
    planet, satellit = line.strip().split(')')
    planeten[planet].append(satellit)


def count_orbits(node, counter, total_sum):
  total_sum += counter
  for satellit in planeten[node]:
    total_sum = count_orbits(satellit,counter+1, total_sum)
  return total_sum  
    

print(count_orbits('COM', 0, 0))
print(time.perf_counter() - time_start)
  