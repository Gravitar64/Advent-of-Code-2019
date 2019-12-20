# Intcode Class Code original by https://www.reddit.com/user/FogleMonster/
# https://www.reddit.com/r/adventofcode/comments/e85b6d/2019_day_9_solutions/faajddr/?context=3

from collections import defaultdict, deque
from Vector import Vec
import time

# ^, v, <, or > for directions
richtungen = {'^': Vec(0, -1), 'v': Vec(0, 1), '<': Vec(-1, 0), '>': Vec(1, 0)}


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
      reads = [(self.mem[x], x, self.mem[x+self.rb])[m]
               for x, m in zip(args, modes)]
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
    if ascii == None:
      return map, robot
    if chr(ascii) in richtungen:
      robot = pos, chr(ascii)
    if ascii == 35:
      map.add(pos)
    x, y = pos
    pos = Vec(x+1, y)
    if ascii == 10:
      pos = Vec(0, y+1)
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
        movement_commands.append(drehung+str(anz_schritte))
        anz_schritte = 0
      neue_richtung = finde_neue_richtung(pos, richt_delta)
      if neue_richtung == None:
        break
      drehung, richt_delta = neue_richtung
  return(movement_commands)

def find_functions(movements):
  movement_functions = defaultdict(str)
  movement_func_commands = ""
  move_encoded, move_encoded_inv = {}, {}
  movements_encoded = ""
  enc_name = 0
  for move in movements:
    if move in move_encoded: continue
    move_encoded[move] = str(enc_name)
    move_encoded_inv[str(enc_name)] = move
    enc_name += 1
  for move in movements:
    movements_encoded += move_encoded[move]
  while True:
    for i in range(1,7):
      move_str = movements_encoded
      func_str = move_str
      a = move_str[:i]
      c = move_str[-i:]
      move_str = move_str.replace(a,'')
      func_str = func_str.replace(a,'A')
      move_str = move_str.replace(c,'')
      func_str = func_str.replace(c,'C')
      b = move_str
      for j in range(1,len(b)):
        b_pat = b.replace(b[:j],'')
        if b_pat == '':
          movement_func_commands = func_str.replace(b[:j],'B')
          movement_functions['A'] = [move_encoded_inv[enc_name] for enc_name in a]
          movement_functions['B'] = [move_encoded_inv[enc_name] for enc_name in b[:j]]
          movement_functions['C'] = [move_encoded_inv[enc_name] for enc_name in c]
    break  
  movement_func_commands = ','.join(movement_func_commands)
  return movement_func_commands, movement_functions

     

intcode = Intcode(program)
map, robot = baue_map(Vec(0, 0))

program[0] = 2
intcode = Intcode(program)
movements = run_scaffold(map, robot)
movement_commands, movement_functions = find_functions(movements)
inputs = """A,B,A,C,B,C,A,B,A,C
R,10,L,8,R,10,R,4
L,6,L,6,R,10
L,6,R,12,R,12,R,10
y
"""
output = []
for char in inputs:
  output.append(intcode.run(ord(char)))
  
# output = intcode.run(10)
# for sektion,moves in movement_functions.items():
#   move_list = []
#   for m in moves:
#     move_list.append(m[:1])
#     move_list.append(m[1:])
#   moves_str = ','.join(move_list)
#   print(moves_str)
#   for char in moves_str:
#     output = intcode.run(ord(char))
#   output = intcode.run(10)
# output = intcode.run(ord('y'))
# output = intcode.run(10)

for _ in range(2500):
  output.append(intcode.run(0))
print(output)



print(f'Lösung = {output} in {time.perf_counter()-start} Sek.')
