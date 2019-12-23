from Vector import Vec
from collections import deque, defaultdict
import itertools as it
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
      elif ord(char) in range(ord('A'), ord('Z')):
        dors[Vec(x, y)] = char.lower()
      elif ord(char) in range(ord('a'), ord('z')):
        keys[Vec(x, y)] = char
      elif char == '@':
        keys[Vec(x, y)] = char
        start_pos = Vec(x,y)

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

def reachable_keys(key, coll_keys, besucht):
  reachable = []
  for v in key2key[key]:
    if v['zu'] in besucht: continue
    if not v['needed'].issubset(coll_keys): continue
    reachable.append((v['dist'],v['zu']))
  #reachable.sort()
  return reachable   

best = 999999

def shortest_way(key, coll_keys, besucht, dist, way):
  global best
  if dist >= best: return
  way.append(key)
  besucht.add(key)
  if len(coll_keys) == len(keys)-1:
    return way,dist
  coll_keys.add(key)
  for d, next_key in reachable_keys(key, coll_keys, besucht):
    erg = shortest_way(next_key, coll_keys.copy(), besucht.copy(), dist+d, way.copy())
    #if komp_way: return True
    if erg:
      w,d = erg
      if d < best:
        best_way = w
        best = d
        print(best, best_way, time.perf_counter()-time_start)


key2key = keys_abstand(keys)
shortest_way('@', set(), set(), 0, [])
#print(best)



