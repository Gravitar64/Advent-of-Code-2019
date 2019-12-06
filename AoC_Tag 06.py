from collections import defaultdict
import time
time_start = time.perf_counter()
#orbits = "COM)B B)C C)D D)E E)F B)G G)H D)I E)J J)K K)L".split()

with open('tag06.txt') as f:
  orbits = f.read().splitlines()

planeten = defaultdict(list)
for orbit in orbits:
  planet, satellit = orbit.split(')')
  planeten[planet].append(satellit)

orbit_counts = {}
def count_orbits(node, counter):
  orbit_counts[node] = counter
  for satellit in planeten[node]:
    count_orbits(satellit,counter+1)

count_orbits('COM', 0)
print(sum(orbit_counts.values()))
print(time.perf_counter() - time_start)
  