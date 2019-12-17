# Code original by https://www.reddit.com/user/FogleMonster/
# https://www.reddit.com/r/adventofcode/comments/e85b6d/2019_day_9_solutions/faajddr/?context=3

from collections import defaultdict
from Vector import Vec
import time
import random as rnd 

a = Vec(0,-1)

richtungen = {1:Vec(0,-1), 2:Vec(0,1), 3:Vec(-1,0), 4:Vec(1,0)}
richt_invers = {1:2, 2:1, 3:4, 4:3}

class State:
  def __init__(self, program):
    self.mem = defaultdict(int, enumerate(program))
    self.ip = 0
    self.rb = 0
    

time_start = time.perf_counter()

with open('Tag15.txt') as f:
  program = list(map(int, f.readline().split(',')))



def run(s, program_input):
  while True:
    op = s.mem[s.ip] % 100
    if op == 99:
      return
    size = [0, 4, 4, 2, 2, 3, 3, 4, 4, 2][op]
    args = [s.mem[s.ip+i] for i in range(1, size)]
    modes = [(s.mem[s.ip] // 10 ** i) % 10 for i in range(2, 5)]
    reads = [(s.mem[x], x, s.mem[x+s.rb])[m] for x, m in zip(args, modes)]
    writes = [(x, None, x+s.rb)[m] for x, m in zip(args, modes)]
    s.ip += size
    if op == 1:
      s.mem[writes[2]] = reads[0] + reads[1]
    if op == 2:
      s.mem[writes[2]] = reads[0] * reads[1]
    if op == 3:
      s.mem[writes[0]] = program_input
    if op == 4:
      return reads[0]
    if op == 5 and reads[0]:
      s.ip = reads[1]
    if op == 6 and not reads[0]:
      s.ip = reads[1]
    if op == 7:
      s.mem[writes[2]] = int(reads[0] < reads[1])
    if op == 8:
      s.mem[writes[2]] = int(reads[0] == reads[1])
    if op == 9:
      s.rb += reads[0]

s = State(program)
  
map = set()
besucht = set()
zufällige_richtungen = [1,2,3,4]
ziel = 0
def labyrinth_lösen(pos_aktuell,letzte_richtung):
  global ziel
  besucht.add(pos_aktuell)
  zuf_richtungen = zufällige_richtungen.copy()
  rnd.shuffle(zuf_richtungen)
  for richt in zuf_richtungen:
    pos_neu = pos_aktuell + richtungen[richt]  
    if pos_neu in besucht or pos_neu in map: continue
    status = run(s,richt)
    if status == 0:
      map.add(pos_neu)
    if status == 2:
      print(f'Found Ziel at {pos_aktuell}')
      if ziel == 0:
        ziel = pos_aktuell
    if status == 1:
      labyrinth_lösen(pos_neu,richt)
  if letzte_richtung != 0:
    status = run(s, richt_invers[letzte_richtung])      
  
start = Vec(21,25)
labyrinth_lösen(start,0)
xse = ([pos[0] for pos in map])
yse = ([pos[1] for pos in map])
max_x, min_x, max_y, min_y = max(xse), min(xse), max(yse), min(yse)
breite, höhe = max_x - min_x, max_y - min_y
print(f'Lösung = {ziel} in {time.perf_counter()-time_start} Sek.')

for y in range(höhe+1):
  print()
  for x in range(breite+1):
    if (x,y) in map:
      print('#', end='')
    elif Vec(x,y) == ziel:
      print('Z', end = '')
    elif Vec(x,y) == start:
      print('S', end = '')
    else:
      print(' ', end = '')         

