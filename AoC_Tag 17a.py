# Intcode Class Code original by https://www.reddit.com/user/FogleMonster/
# https://www.reddit.com/r/adventofcode/comments/e85b6d/2019_day_9_solutions/faajddr/?context=3

from collections import defaultdict, deque
from Vector import Vec
import time
import itertools as iter


# ^, v, <, or > for directions
richtungen = {'^': Vec(0, -1), 'v': Vec(0, 1), '<': Vec(-1, 0), '>': Vec(1, 0)}


class Intcode:
  def __init__(self, program):
    self.mem = defaultdict(int, enumerate(program))
    self.ip = 0
    self.rb = 0
    self.input = []
    self.output = []

  def load_input(self,data):
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


def baue_karte(output, pos):
  karte = set()
  for o in output:
    o = chr(o)
    if o in richtungen:
      robot = pos, o
    if o == '#':
      karte.add(pos)
    x, y = pos
    pos = Vec(x+1, y)
    if o == '\n':
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

def finde_funktionen(moves):
  mov = [moves[i]+moves[i+1] for i in range(0, len(moves),2)]
  mov_str = ''.join(mov)
  übersetzung = {m:chr(65+i) for i,m in enumerate(set(mov))}
  for alt, neu in übersetzung.items():
    mov_str = mov_str.replace(alt,neu)
  while True:
    for i in range(1,5):
      m = mov_str
      a = m[:i]
      c = m[-i:]
      m = m.replace(a,'').replace(c,'')
      b_pat = m
      for j in range(1,5):
        b = b_pat.replace(b_pat[:j],'')
        if not b:
          return (a,b_pat[:j],c), mov_str, übersetzung

def generiere_program_input(patterns, mov_str, übersetzung):
  ü_inv = {v:k for k,v in übersetzung.items()}
  program_input = mov_str.replace(patterns[0],'A,').replace(patterns[1],'B,').replace(patterns[2],'C,')[:-1]+'\n'
  for pattern in patterns:
    program_input += ','.join([ü_inv[a][:1]+','+ü_inv[a][1:] for a in pattern])+'\n'
  program_input += 'n\n'
  return program_input  


intcode = Intcode(program)
intcode.run()
karte, robot = baue_karte(intcode.output, Vec(0, 0))
movements = run_scaffold(karte, robot)
patterns, mov_str, übersetzung = finde_funktionen(movements)
program_input = generiere_program_input(patterns, mov_str, übersetzung)

program[0] = 2
intcode = Intcode(program)
intcode.load_input([ord(x) for x in program_input])
intcode.run()
lösung = intcode.output[-1]  

print(f'Lösung = {lösung} in {time.perf_counter()-start} Sek.')
