from Vector import Vec
from collections import deque, defaultdict
import itertools as it

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
  
  key2key = {}
  for pos in keys:
    counter = 0
    key1 = keys[pos]
    visited, stack = set([pos]), deque([[pos, counter, []]])
    while stack:
      pos, counter, way = stack.popleft()
      if pos in keys:
        key2 = keys[pos]
        if key1 != key2:
          needed_dors = set()
          for p in way:
            if p not in dors:
              continue
            needed_dors.add(dors[p])
          key2key[key1+key2] = {'dist': counter, 'needed': needed_dors}
      visited.add(pos)
      way.append(pos)
      for nachb in find_nachbarn(pos):
        if nachb in visited:
          continue
        stack.append([nachb, counter + 1, way.copy()])
  return key2key    

key2key = keys_abstand(keys)

possible_keys = []
for key in keys.values():
  if key == '@':
    continue
  abst_key = '@'+key
  needed = len(key2key[abst_key]['needed'])
  dist = key2key[abst_key]['dist']
  possible_keys.append((needed, dist, key))
possible_keys.sort()

possible_keys = [x[2] for x in possible_keys]
best = 999999
# for _ in range(1):
for perm in it.permutations(possible_keys):
  if key2key[perm[0]+perm[1]]['needed']:
    continue
  perm2 = ('@',) + perm
  summe = 0
  valid = True
  collected_keys = set()

  for i in range(0, len(perm2)-1):
    p = perm2[i]+perm2[i+1]
    #print(collected_keys,p[0], p[1])
    if p[0] in dors_inv:
      collected_keys.add(p[0])
    if not key2key[p]['needed'].issubset(collected_keys):
      valid = False
      break
    #print(perm2, p, key2key[p]['needed'], collected_keys)
    summe += key2key[p]['dist']
  if valid and summe < best:
    best = summe
    print(f'Best Way {perm2} mit {summe} Schritten')
