# Code original by https://www.reddit.com/user/FogleMonster/
# https://www.reddit.com/r/adventofcode/comments/e85b6d/2019_day_9_solutions/faajddr/?context=3

from collections import defaultdict
from Vector import Vec
import time

#north (1), south (2), west (3), and east (4).
richtungen = {1:Vec(0,-1), 2:Vec(0,1), 3:Vec(-1,0), 4:Vec(1,0)}
richt_invers = {1:2, 2:1, 3:4, 4:3} 

class State:
  def __init__(self, program):
    self.mem = defaultdict(int, enumerate(program))
    self.ip = 0
    self.rb = 0
    

start = time.perf_counter()

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

weg = []
map = set()
besucht = set()


def labyrinth_lösen(pos_aktuell, vorherige_Richtung):
  besucht.add(pos_aktuell)
  for richt, delta in richtungen.items():
    neue_pos = pos_aktuell + delta
    if neue_pos in besucht: continue
    status = run(s, richt)
    if status == 0:
      map.add(neue_pos)
    elif status == 2:
      print(f'Oxygen-Tank gefunden auf Pos {neue_pos}')
      weg.append(neue_pos)
      return True  
    elif status == 1:
      if labyrinth_lösen(neue_pos, richt):
        weg.append(neue_pos)
        return True
  status = run(s, richt_invers[vorherige_Richtung])
  if status != 1:
    print(f'ERROR! Zurück von Pos {pos_aktuell} mit Richtung {rich_invers[vorherige_Richtung]} lieferte den Status {status}')

s = State(program)
labyrinth_lösen(Vec(0,0), 1)
lösung = len(weg)


print(f'Lösung = {lösung} in {time.perf_counter()-start} Sek.')



