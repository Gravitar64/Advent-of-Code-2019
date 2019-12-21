# Intcode Class Code original by https://www.reddit.com/user/FogleMonster/
# https://www.reddit.com/r/adventofcode/comments/e85b6d/2019_day_9_solutions/faajddr/?context=3

from collections import defaultdict, deque
from Vector import Vec
import time

#^, v, <, or > for directions
richtungen = {'^':Vec(0,-1), 'v':Vec(0,1), '<':Vec(-1,0), '>':Vec(1,0)}


class Intcode:
  def __init__(self, program):
    self.mem = defaultdict(int, enumerate(program))
    self.ip = 0
    self.rb = 0

  def run(self, program_input):
    while True:
      op = self.mem[self.ip] % 100
      if op == 99:
        return
      size = [0, 4, 4, 2, 2, 3, 3, 4, 4, 2][op]
      args = [self.mem[self.ip+i] for i in range(1, size)]
      modes = [(self.mem[self.ip] // 10 ** i) % 10 for i in range(2, 5)]
      reads = [(self.mem[x], x, self.mem[x+self.rb])[m] for x, m in zip(args, modes)]
      writes = [(x, None, x+self.rb)[m] for x, m in zip(args, modes)]
      self.ip += size
      if op == 1:
        self.mem[writes[2]] = reads[0] + reads[1]
      if op == 2:
        self.mem[writes[2]] = reads[0] * reads[1]
      if op == 3:
        self.mem[writes[0]] = program_input
      if op == 4:
        return reads[0]
      if op == 5 and reads[0]:
        self.ip = reads[1]
      if op == 6 and not reads[0]:
        self.ip = reads[1]
      if op == 7:
        self.mem[writes[2]] = int(reads[0] < reads[1])
      if op == 8:
        self.mem[writes[2]] = int(reads[0] == reads[1])
      if op == 9:
        self.rb += reads[0]  
    
start = time.perf_counter()
with open('Tag17.txt') as f:
  program = list(map(int, f.readline().split(',')))

def baue_map(pos):
  map = set()  
  while True:
    ascii = intcode.run(0)
    if ascii == None: return map, robot
    if chr(ascii) in richtungen:
      robot = pos, chr(ascii)
    if ascii == 35: map.add(pos)
    x,y = pos
    pos = Vec(x+1, y)
    if ascii == 10: pos = Vec(0, y+1)   
  return map
def finde_neue_richtung(pos, richt):
  x, y = richt
  for drehung in ['L', 'R']:
    if drehung == 'L':
      x1, y1 = y*1, x*-1
    else:
      x1, y1 = y*-1, x * 1
    if pos + Vec(x1, y1) in map:
      return drehung, Vec(x1, y1)
def run_scaffold(map, robot):
  pos, dir_indicator = robot
  richt_delta = richtungen[dir_indicator]
  movement_commands = []
  anz_schritte = 0
  while True:
    neue_pos = pos + richt_delta
    if neue_pos in map:
      pos = neue_pos
      anz_schritte += 1
    else:
      if anz_schritte > 0:
        movement_commands.extend([drehung, str(anz_schritte)])
        anz_schritte = 0
      neue_richtung = finde_neue_richtung(pos, richt_delta)
      if neue_richtung == None:
        break
      drehung, richt_delta = neue_richtung
  return(movement_commands)


intcode = Intcode(program)
map, robot = baue_map(Vec(0,0))
movements = run_scaffold(map, robot)
print(movements)

#print(f'Lösung = {lösung} in {time.perf_counter()-start} Sek.')
