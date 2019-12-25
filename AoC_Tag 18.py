from Vector import Vec
from collections import deque, defaultdict
import time
import random as rnd

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
        start_pos = Vec(x, y)
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
      if neue_pos in walls: continue
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
          needkeys = set()
          for p in way:
            if p not in dors:
              continue
            needkeys.add(dors[p])
          key2key[key1].append((key2, counter, needkeys))
      visited.add(pos)
      way.append(pos)
      for nachb in find_nachbarn(pos):
        if nachb in visited:
          continue
        stack.append([nachb, counter + 1, way.copy()])
  return key2key


def reachable_keys(key, havekeys):
  reachable = []
  for zu, dist, needkeys in key2key[key]:
    if zu in havekeys:
      continue
    if not needkeys.issubset(havekeys):
      continue
    reachable.append((dist,zu))
  #reachable.sort()
  return reachable


cache = {}


def shortest_way(key, havekeys):
  coll_str = ''.join(sorted(list(havekeys)))
  if (key, coll_str) in cache:
    return cache[key, coll_str]
  keys = reachable_keys(key, havekeys)
  if not keys:
    ans = 0
  else:
    ergebnisse = []
    for d, next_key in keys:
      havekeys.add(next_key)
      ergebnisse.append(d + shortest_way(next_key, havekeys))
      havekeys.remove(next_key)
    ans = min(ergebnisse)
  cache[key, coll_str] = ans
  return ans


key2key = keys_abstand(keys)
print(
    f'Lösung = {shortest_way("@", set())} Steps in {time.perf_counter()-time_start} Sek.'
)
