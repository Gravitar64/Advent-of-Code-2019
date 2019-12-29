from collections import deque
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


def lieferPortalBezeichnung(pos):
  portalBezeichnung = ''
  for r in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
    x, y = pos
    while True:
      x, y = x+r[0], y+r[1]
      if (x, y) in portal_buchstaben:
        portalBezeichnung += portal_buchstaben[x, y]
      else:
        break
  return ''.join(sorted(portalBezeichnung))


def ermittelPortale(weg):
  portals = {pos: lieferPortalBezeichnung(
      pos) for pos in weg if lieferPortalBezeichnung(pos)}
  portals_inv = {v: k for k, v in portals.items()}
  start, ziel = portals_inv['AA'], portals_inv['ZZ']
  for pos1, portal1 in portals.items():
    for pos2, portal2 in portals.items():
      if pos1 == pos2:
        continue
      if portal1 == portal2:
        portals[pos1] = pos2
        portals[pos2] = pos1
  del portals[start]
  del portals[ziel]
  return start, ziel, portals


def bfs(weg, start, ziel):
  visited, stack = set(), deque([[start, 0]])
  while stack:
    pos, dist = stack.popleft()
    if pos in visited:
      continue
    if pos == ziel:
      return dist
    visited.add(pos)
    if pos in portals:
      stack.append([portals[pos], dist+1])
    for r in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
      nachbar = pos[0]+r[0], pos[1]+r[1]
      if nachbar not in weg:
        continue
      stack.append([nachbar, dist+1])


start, ziel, portals = ermittelPortale(weg)
print(f'Lösung = {bfs(weg, start, ziel)} in {time.perf_counter() - time_start} Sek.')
