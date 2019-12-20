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
    self.input = []
    self.output = []

  def load_inputs(self, data):
    self.input.extend(data)

  def run(self):
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
        self.mem[writes[0]] = self.input.pop(0)
      if op == 4:
        self.output.append(reads[0])
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


def baue_map(data):
  karte = set()
  pos = Vec(0, 0)
  for element in data:
    e = chr(element)
    if e in richtungen:
      robot = pos, e
    if e == '#':
      karte.add(pos)
    x, y = pos
    pos = Vec(x+1, y)
    if e == '\n':
      pos = Vec(0, y+1)
  return karte, robot


def finde_neue_richtung(pos, richt):
  x, y = richt
  for drehung in ['L', 'R']:
    if drehung == 'L':
      x1, y1 = y*1, x*-1
    else:
      x1, y1 = y*-1, x * 1
    if pos + Vec(x1, y1) in karte:
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


def generate_inputs(patterns, enc_str, trans):
  trans_invers = {v: k for k, v in trans.items()}
  main_routine = enc_str.replace(patterns[0], 'A,').replace(
      patterns[1], 'B,').replace(patterns[2], 'C,')[:-1]
  func_a = ','.join([trans_invers[a][:1]+','+trans_invers[a][1:]
                     for a in patterns[0]])
  func_b = ','.join([trans_invers[a][:1]+','+trans_invers[a][1:]
                     for a in patterns[1]])
  func_c = ','.join([trans_invers[a][:1]+','+trans_invers[a][1:]
                     for a in patterns[2]])
  return main_routine + '\n' + func_a + '\n' + func_b + '\n' + func_c + '\n' + 'n\n'


def find_functions(moves):
  mov = [moves[i]+moves[i+1] for i in range(0, len(moves), 2)]
  mov_str = mov_enc_str = ''.join(mov)
  mov_enc, mov_enc_inv = {}, {}
  enc = 65
  for move in mov:
    if move in mov_enc:
      continue
    mov_enc[move] = chr(enc)
    enc += 1
  for old, new in mov_enc.items():
    mov_enc_str = mov_enc_str.replace(old, new)
  while True:
    for i in range(1, 7):
      move_str = mov_enc_str
      a = move_str[:i]
      c = move_str[-i:]
      move_str = move_str.replace(a, '').replace(c, '')
      b = move_str
      for j in range(1, len(b)):
        b_pat = b.replace(b[:j], '')
        if b_pat == '':
          program_inputs = generate_inputs((a, b[:j], c), mov_enc_str, mov_enc)
    break
  mov_enc_inv = {v: k for k, v in mov_enc.items()}
  return program_inputs


intcode = Intcode(program)
intcode.run()
karte, robot = baue_map(intcode.output)

program[0] = 2
intcode = Intcode(program)
moves = run_scaffold(karte, robot)
inputs = find_functions(moves)
intcode.load_inputs([ord(x) for x in inputs])
intcode.run()
lösung = intcode.output[-1]

print(f'Lösung = {lösung} in {time.perf_counter()-start} Sek.')
