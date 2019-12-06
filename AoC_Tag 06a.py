from collections import defaultdict
import time
time_start = time.perf_counter()

nodes = defaultdict(list)
with open('tag06.txt') as f:
  for line in f.readlines():
    von, zu = line.strip().split(')')
    nodes[von].append(zu)
    nodes[zu].append(von)
    if zu == "YOU":
      start = von
    if zu == "SAN":
      ziel = von

besucht = set()
def find_way(node, counter):
  besucht.add(node)
  if node == ziel:
    print(counter)
    return True
  for next_node in nodes[node]:
    if next_node in besucht: continue
    if find_way(next_node, counter+1):
      return True 
  

find_way(start,0)
print(time.perf_counter() - time_start)
  