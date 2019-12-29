from collections import deque
import time

time_start = time.perf_counter()

weg = set()
portal_buchstaben = {}
with open('tag20.txt') as f:
  for y,line in enumerate(f):
    for x,char in enumerate(line.rstrip('\n')):
      if char == '.':
        weg.add((x,y))
      if char.isupper():
        portal_buchstaben[x,y] = char

def getPortal(pos):
  richtungen = [(0,1), (0,-1), (1,0), (-1,0)]
  portal = set()
  for r in richtungen:
    x,y = pos
    while True:
      x,y = x+r[0], y+r[1]
      if (x,y) in portal_buchstaben:
        portal.add(portal_buchstaben[x,y])
      else:
        break
  return portal        
  

portals = {}
for pos in weg:
  ans = getPortal(pos)
  if not ans: continue
  portals[pos] = ans
for pos1,portal1 in portals.items():
  if portal1 == set('A'):
    start_pos = pos1
    continue
  if portal1 == set('Z'):
    ziel_pos = pos1
    continue
  for pos2,portal2 in portals.items():
    if pos1 == pos2: continue
    if portal1 == portal2:
      portals[pos1] = pos2
      portals[pos2] = pos1
del portals[start_pos]
del portals[ziel_pos]

def nachbarn(weg, pos):
  richtungen = [(0,1), (0,-1), (1,0), (-1,0)]
  nachb = []
  for r in richtungen:
    neupos = pos[0]+r[0], pos[1]+r[1]
    if neupos in weg:
      nachb.append(neupos)
  return nachb   


def bfs(weg,start,ziel):
  visited, stack = set(), deque([[start,0]])
  while stack:
    pos, dist = stack.popleft()
    visited.add(pos)
    if pos in portals:
      pos = portals[pos]
      dist += 1
      visited.add(pos)  
    if pos == ziel:
      return dist
    for nachbar in nachbarn(weg,pos):
      if nachbar in visited: continue
      stack.append([nachbar,dist+1])

print(f'Lösung = {bfs(weg,start_pos,ziel_pos)} in {time.perf_counter() - time_start} Sek.')



    
