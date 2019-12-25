from Vector import Vec
from collections import deque, defaultdict
import itertools as it
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
          needed = set()
          for p in way:
            if p not in dors:
              continue
            needed.add(dors[p])
          key2key[key1].append((key2, counter, needed))
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
      continue #den ziel-key habe ich schon, da brauche ich nicht mehr hin
    if not needkeys.issubset(havekeys):
      continue #ich habe nicht alle keys (havekeys), die ich für diesen ziel-key benötige (needkeys)
    reachable.append((dist, zu))
  return reachable


seen = {}
def minwalk(start, havekeys):
  hks = ''.join(sorted(list(havekeys)))
  if (start, hks) in seen:
    return seen[start, hks]
  keys = reachable_keys(start, havekeys)
  if not keys:
    # done!
    ans = 0
  else:
    poss = []
    for dist, ch in keys:
      #print(start, ch, havekeys, dist)
      havekeys.add(ch)
      walk_dist = dist + minwalk(ch, havekeys)
      havekeys.remove(ch)
      poss.append(walk_dist)
    ans = min(poss)
  seen[start, hks] = ans
  return ans


key2key = keys_abstand(keys)

print(minwalk('@', set()), time.perf_counter()-time_start)


#print(f'Steps={best} in {time.perf_counter()-time_start:.2f} Sek -> {best_way}')
