from collections import defaultdict
#orbits = "COM)B B)C C)D D)E E)F B)G G)H D)I E)J J)K K)L K)YOU I)SAN".split()

with open('tag06.txt') as f:
  orbits = f.read().splitlines()

planeten = defaultdict(list)
satelliten = defaultdict(str)
for orbit in orbits:
  planet, satellit = orbit.split(')')
  satelliten[satellit] = planet
  planeten[planet].append(satellit)
  if satellit == "YOU":
    start = planet
  if satellit == "SAN":
    ziel = planet

for satellit in satelliten:
  planet = satelliten[satellit]
  planeten[satellit].append(planet)


besucht = set()
def find_way(node, counter):
  if node == ziel:
      print(counter)
      return True
  besucht.add(node)
  counter += 1
  for next_node in planeten[node]:
    if next_node in besucht: continue
    if find_way(next_node, counter):
      return True  
  

find_way(start,0)
  