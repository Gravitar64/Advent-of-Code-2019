from collections import defaultdict
import time
time_start = time.perf_counter()
#orbits = "COM)B B)C C)D D)E E)F B)G G)H D)I E)J J)K K)L K)YOU I)SAN".split()

with open('tag06.txt') as f:
  orbits = f.read().splitlines()

planeten = defaultdict(list)
for orbit in orbits:
  planet, satellit = orbit.split(')')
  planeten[planet].append(satellit)
  planeten[satellit].append(planet)
  if satellit == "YOU":
    start = planet
  if satellit == "SAN":
    ziel = planet

besucht = set()
def find_way(node, counter):
  besucht.add(node)
  if node == ziel:
    print(counter)
    return True
  for next_node in planeten[node]:
    if next_node in besucht: continue
    if find_way(next_node, counter+1):
      return True  
  

find_way(start,0)
print(time.perf_counter() - time_start)
  