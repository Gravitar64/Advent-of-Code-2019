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

# def get_sequenz(s):
#   sequenz = []
#   for _ in range(3):
#     output = run(s,0)
#     if output == None:
#       return
#     sequenz.append(output)
#   return sequenz    

s = State(program)
  
map = set()
weg = []
besucht = set()
zufällige_richtungen = [1,2,3,4]
def labyrinth_lösen(pos_aktuell,letzte_richtung):
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
      weg.append(pos_aktuell)
      print(f'Found Ziel at {pos_aktuell}')
      return True
    if status == 1:
      if labyrinth_lösen(pos_neu,richt):
        if pos_neu not in weg:
          weg.append(pos_neu)
        return True
  status = run(s, richt_invers[letzte_richtung])      
  
labyrinth_lösen(Vec(21,25),0)

print(f'Lösung = {len(weg)} in {time.perf_counter()-start} Sek.')

