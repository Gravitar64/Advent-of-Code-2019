# Code original by https://www.reddit.com/user/FogleMonster/
# https://www.reddit.com/r/adventofcode/comments/e85b6d/2019_day_9_solutions/faajddr/?context=3

from collections import defaultdict, Counter
from Vector import Vec
import time

richt = {'u':Vec(0,-1), 'd': Vec(0,1), 'r': Vec(1,0), 'l': Vec(-1,0)}
richt_wechsel = {'u':['l','r'], 'd':['r','l'], 'r':['u','d'], 'l':['d','u']}

class State:
  def __init__(self, program):
    self.mem = defaultdict(int, enumerate(program))
    self.ip = 0
    self.rb = 0
    

start = time.perf_counter()

with open('Tag11.txt') as f:
  program = list(map(int, f.readline().split(',')))

s = State(program)

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

pos = Vec(0,0)
rob_richt = 'u'
panels = defaultdict(int)
gemalt = Counter()
while True:
  farbe = run(s,panels[pos])
  if farbe == None:
    break
  gemalt[pos] += 1
  rob_richt = richt_wechsel[rob_richt][run(s,farbe)]
  panels[pos] = farbe
  pos += richt[rob_richt]

print(len(gemalt))
print(time.perf_counter()-start)


