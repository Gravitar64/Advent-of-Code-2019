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
höhe, breite = y,x        

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
  portals = {pos: [lieferPortalBezeichnung(pos)] for pos in weg if lieferPortalBezeichnung(pos)}
  portal_invers = {v[0]:k for k,v in portals.items()}
  start, ziel = portal_invers['AA'], portal_invers['ZZ']
  del portals[start]
  del portals[ziel]
  for pos1, portal1 in portals.items():
    for pos2, portal2 in portals.items():
      if pos1 == pos2: continue
      if portal1 == portal2:
        portals[pos1].append(pos2)
        portals[pos2].append(pos1)
  for x,y in portals:
    level = -1 if x in (2,breite-2) or y in (2,höhe-2) else 1
    portals[x,y].append(level)
  return start, ziel, portals

def bfs(start,ziel,weg,portals):
  level = 0
  besucht, stack = set(), deque([[start,0,level]])
  while stack:
    pos, dist,level = stack.popleft()
    if (pos,level) in besucht or level < 0:
      continue
    if pos == ziel and level == 0:
      return dist
    besucht.add((pos,level))
    if pos in portals:
      name, sprungziel, lv = portals[pos]
      stack.append([sprungziel, dist + 1, level+lv])
    for richtung in [(0,1), (0,-1), (-1,0), (1,0)]:
      nachbar = pos[0] + richtung[0], pos[1]+richtung[1]
      if nachbar not in weg: continue
      stack.append([nachbar, dist+1,level])

start, ziel, portals = ermittelPortale(weg)
print(f'Lösung = {bfs(start,ziel,weg,portals)} Steps in {time.perf_counter()-time_start} Sek.')


