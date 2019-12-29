from collections import deque, defaultdict
import time

time_start = time.perf_counter()

weg = set()
portal_buchstaben = {}
with open('tag20.txt') as f:
  for y, line in enumerate(f):
    for x, char in enumerate(line.rstrip('\n')):
      if char == '.':
        weg.add((x, y))
      if char.isupper():
        portal_buchstaben[x, y] = char
width, height = x, y


def getPortal(pos):
  portal = set()
  for r in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
    x, y = pos
    while True:
      x, y = x+r[0], y+r[1]
      if (x, y) in portal_buchstaben:
        portal.add(portal_buchstaben[x, y])
      else:
        break
  return portal


def finde_portale(weg):
  portals = defaultdict(list)
  for pos in weg:
    ans = getPortal(pos)
    if not ans:
      continue
    portals[pos].append(ans)
  for pos1, portal1 in portals.items():
    if portal1[0] == {'A'}:
      start = pos1
      continue
    if portal1[0] == {'Z'}:
      ziel = pos1
      continue
    for pos2, portal2 in portals.items():
      if pos1 == pos2:
        continue
      if portal1 == portal2:
        portals[pos1].append(pos2)
        portals[pos2].append(pos1)

  del portals[start]
  del portals[ziel]

  for pos in portals:
    x, y = pos
    if x in (2, width-2) or y in (2, height-2):
      level = -1
    else:
      level = 1
    portals[pos].append(level)
  return start, ziel, portals


def nachbarn(weg, pos):
  for r in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
    nachbar = pos[0]+r[0], pos[1]+r[1]
    if nachbar not in weg:
      continue
    yield nachbar


def bfs(portals, weg, start, ziel):
  level = 0
  visited, stack = set((start, 0)), deque([[start, 0, level]])
  while stack:
    pos, dist, level = stack.popleft()
    if level < 0 or (pos, level) in visited:
      continue
    visited.add((pos, level))
    if pos == ziel and level == 0:
      print('Solution found', level, pos, ziel)
      return dist
    for nachbar in nachbarn(weg, pos):
      stack.append([nachbar, dist+1, level])
    if pos in portals:
      name, p, lv = portals[pos]
      stack.append([p, dist+1, level+lv])


start, ziel, portals = finde_portale(weg)
print(
    f'Lösung = {bfs(portals,weg,start,ziel)} in {time.perf_counter() - time_start} Sek.')
