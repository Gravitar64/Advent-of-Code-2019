from Vector import Vec
import time
from collections import defaultdict

time_start = time.perf_counter()

map = set()
with open("tag10.txt") as f:
  for y, line in enumerate(f):
    for x, zeichen in enumerate(line):
      if zeichen != '#': continue
      map.add(Vec(x,y))

start = Vec(14,17)
angles = defaultdict(list)

for asteroid in map:
  angle = 360 - start.winkel(asteroid)
  angle = 0 if angle == 360 else angle
  angles[angle].append(asteroid)

sort_by_angle = [angles[angle] for angle in sorted(angles.keys())]

destroyed = 0
fertig = False
while not fertig:
  for angle in sort_by_angle:
    asteroid = angle.pop()
    destroyed += 1
    if destroyed == 200:
      print(asteroid[0] * 100 + asteroid[1])
      fertig = True
      break

print(time.perf_counter() - time_start)
