from collections import deque
import time

time_start = time.perf_counter()

weg = set()
portal_buchstaben = {}
with open('tag20.txt') as f:
  for y, zeile in enumerate(f):
    for x, zeichen in enumerate(zeile.rstrip('\n')):
      if zeichen == '.':
        weg.add((x,y))
      elif zeichen.isupper():
        portal_buchstaben[x,y] = zeichen

def lieferPortalBezeichnung(pos):
  portalBezeichnung = ''
  for richtung in [(0,1), (0,-1), (-1,0), (1,0)]:
    x,y = pos
    while True:
      x,y = x+richtung[0], y+richtung[1]
      if (x,y) in portal_buchstaben:
        portalBezeichnung += portal_buchstaben[x,y]
      else:
        break
  return ''.join(sorted(portalBezeichnung))

def ermittelPortale(weg):
  portals = {pos: lieferPortalBezeichnung(pos) for pos in weg if lieferPortalBezeichnung(pos)}
  portal_invers = {v:k for k,v in portals.items()}
  start, ziel = portal_invers['AA'], portal_invers['ZZ']
  del portals[start]
  del portals[ziel]
  for pos1, portal1 in portals.items():
    for pos2, portal2 in portals.items():
      if pos1 == pos2: continue
      if portal1 == portal2:
        portals[pos1] = pos2
        portals[pos2] = pos1
  return start, ziel, portals

def bfs(start,ziel,weg):
  besucht, stack = set(), deque([[start,0]])
  while stack:
    pos, dist = stack.popleft()
    if pos in besucht:
      continue
    if pos == ziel:
      return dist
    besucht.add(pos)
    if pos in portals:
      stack.append([portals[pos], dist + 1])
    for richtung in [(0,1), (0,-1), (-1,0), (1,0)]:
      nachbar = pos[0] + richtung[0], pos[1]+richtung[1]
      if nachbar not in weg: continue
      stack.append([nachbar, dist+1])

start, ziel, portals = ermittelPortale(weg)
print(f'Lösung = {bfs(start,ziel,weg)} Steps in {time.perf_counter()-time_start} Sek.')


