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

start = Vec(14,17)
map.remove(start)

winkels = defaultdict(list)

for asteroid in map:
  winkel = 360 - start.winkel(asteroid)
  winkel = 0 if winkel == 360 else winkel
  winkels[winkel].append(asteroid)

sortiert_nach_winkel = [winkels[winkel] for winkel in sorted(winkels.keys())]

zerstört = 0
fertig = False
while not fertig:
  for asteroiden in sortiert_nach_winkel:
    asteroid = asteroiden.pop()
    zerstört += 1
    if zerstört == 200:
      lösung = asteroid[0]*100 + asteroid[1]
      fertig = True
      break


print(f'Lösung: {lösung} ermittelt in {time.perf_counter()-time_start:0.3f} Sek.')