from Vector import Vec
from collections import defaultdict
import time

time_start = time.perf_counter()

map = set()
with open("tag10.txt") as f:
  for y, zeile in enumerate(f):
    for x, zeichen in enumerate(zeile):
      if zeichen != '#': continue
      map.add(Vec(x,y))

winkels = defaultdict(set)
for asteroid1 in map:
  for asteroid2 in map:
    if asteroid1 == asteroid2: continue
    winkels[asteroid1].add(asteroid1.winkel(asteroid2))

lösung = sorted([(len(winkel), pos) for pos, winkel in winkels.items()])[-1]

print(f'Lösung: {lösung} ermittelt in {time.perf_counter()-time_start:0.3f} Sek.')