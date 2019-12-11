from Vector import Vec
from collections import defaultdict
import time

time_start = time.perf_counter()

map = set()
with open("tag10.txt") as f:
  for y, line in enumerate(f):
    for x, zeichen in enumerate(line):
      if zeichen != '#': continue
      map.add(Vec(x,y))

angles = defaultdict(set)

for a1 in map:
  for a2 in map:
    if a1 == a2: continue
    angles[a1].add(a1.winkel(a2))

best_pos = sorted([(len(value), key) for key,value in angles.items()])[-1]

print (best_pos)
print(time.perf_counter() - time_start)
