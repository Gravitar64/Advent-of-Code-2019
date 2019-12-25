from Vector import Vec
from collections import deque,defaultdict
import time

time_start = time.perf_counter()


walls = set()
keys = {}
dors = {}
with open("tag18.txt") as f:
  for y, line in enumerate(f):
    for x, char in enumerate(line.strip()):
      if char == '#':
        walls.add(Vec(x, y))
      elif char == '@':
        keys[Vec(x, y)] = char
        start_pos = Vec(x,y)
      elif char.isupper():
        dors[Vec(x, y)] = char.lower()
      elif char.islower():
        keys[Vec(x, y)] = char

dors_inv = {v: k for k, v in dors.items()}


def keys_abstand(keys):
  
  def find_nachbarn(pos):
    richtungen = [Vec(1, 0), Vec(-1, 0), Vec(0, 1), Vec(0, -1)]
    nachb = []
    for richt in richtungen:
      neue_pos = pos + richt
      if neue_pos not in walls:
        nachb.append(neue_pos)
    return nachb
  
  key2key = defaultdict(list)
  for pos in keys:
    counter = 0
    key1 = keys[pos]
    visited, stack = set([pos]), deque([[pos, counter, []]])
    while stack:
      pos, counter, way = stack.popleft()
      if pos in keys:
        key2 = keys[pos]
        if key1 != key2 and key2 != '@':
          needed_dors = set()
          for p in way:
            if p not in dors:
              continue
            needed_dors.add(dors[p])
          key2key[key1] += [{'zu':key2,'dist': counter, 'needed': needed_dors}]
      visited.add(pos)
      way.append(pos)
      for nachb in find_nachbarn(pos):
        if nachb in visited:
          continue
        stack.append([nachb, counter + 1, way.copy()])
  return key2key    

def reachable_keys(key, coll_keys):
  reachable = []
  for v in key2key[key]:
    if v['zu'] in coll_keys: continue
    if not v['needed'].issubset(coll_keys): continue
    reachable.append((v['dist'],v['zu']))
  #reachable.sort()
  return reachable   


cache = {}
def shortest_way(key, coll_keys):
  coll_str = ''.join(sorted(list(coll_keys)))
  if (key,coll_str) in cache:
    return cache[key,coll_str]
  keys = reachable_keys(key, coll_keys)
  if not keys:
    ans = 0
  else:
    ergebnisse = []
    for d, next_key in keys:
      coll_keys.add(next_key)  
      ergebnisse.append(d + shortest_way(next_key, coll_keys))
      coll_keys.remove(next_key)
    ans = min(ergebnisse)  
  cache[key,coll_str] = ans
  return ans  

key2key = keys_abstand(keys)
print(shortest_way('@', set()),time.perf_counter()-time_start)