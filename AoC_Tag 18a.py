from collections import deque

with open('tag18_2.txt') as f:
  walls = set()
  keys, dors = {}, {}
  starts = []
  for y,zeile in enumerate(f):
    for x, char in enumerate(zeile.strip()):
      if char == '@':
        starts.append((x,y))
      elif char == '#':
        walls.add((x,y))
      elif char.islower():
        keys[x,y] = char
      elif char.isupper():
        dors[x,y] = char.lower()

def nachbarn(pos):
  richtungen = [(0,1), (0,-1), (1,0), (-1,0)]
  for r in richtungen:
    nachbar = pos[0] + r[0], pos[1] + r[1]
    if nachbar in walls: continue
    yield nachbar

def erreichbare_schlüssel(pos, gesammelte_schlüssel):
  stack = deque([pos])
  visited = {pos: 0}
  erreichbareSchlüssel = {}
  while stack:
    pos = stack.popleft()
    for nachb in nachbarn(pos):
      if nachb in visited: continue
      visited[nachb] = visited[pos]+1
      if nachb in dors and dors[nachb] not in gesammelte_schlüssel: continue
      if nachb in keys and keys[nachb] not in gesammelte_schlüssel:
        erreichbareSchlüssel[keys[nachb]] = visited[nachb], nachb
      else:
        stack.append(nachb)
  return erreichbareSchlüssel

def wähleStartaus4(starts, gesammelte_schlüssel):
  erreichbareSchlüssel = {}
  for rob_id, start in enumerate(starts):
    for char, (dist, pos) in erreichbare_schlüssel(start, gesammelte_schlüssel).items():
      erreichbareSchlüssel[char]= dist, pos, rob_id
  return erreichbareSchlüssel      

cache = {}
def kürzester_weg(starts, gesammelte_schlüssel):
  cache_str = ''.join(sorted(gesammelte_schlüssel))
  if (starts,cache_str) in cache:
    return cache[starts,cache_str]
  erreichbareSchlüssel = wähleStartaus4(starts, gesammelte_schlüssel)
  if not erreichbareSchlüssel:
    erg = 0
  else:
    ergebnisse = []
    for char, (dist, pos, rob_id) in erreichbareSchlüssel.items():
      nstarts = tuple(pos if i == rob_id else p for i,p in enumerate(starts))
      ergebnisse.append(dist + kürzester_weg(nstarts, gesammelte_schlüssel+char))
    erg = min(ergebnisse)
  cache[starts,cache_str] = erg  
  return erg

print(kürzester_weg(tuple(starts),''))        