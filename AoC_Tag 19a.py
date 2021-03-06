# Intcode Class Code original by https://www.reddit.com/user/FogleMonster/
# https://www.reddit.com/r/adventofcode/comments/e85b6d/2019_day_9_solutions/faajddr/?context=3

from collections import defaultdict, deque
from Vector import Vec
import time



class Intcode:
  def __init__(self, program):
    self.mem = defaultdict(int, enumerate(program))
    self.ip = 0
    self.rb = 0
    self.input = []
    self.output = []

  def reset(self):
    self.ip, self.rb = 0,0
    self.mem = defaultdict(int, enumerate(program))
    
  
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
with open('Tag19.txt') as f:
  program = list(map(int, f.readline().split(',')))

def inTraktorStrahl(intcode, x, y):
  intcode.load_input([x,y])
  intcode.run()
  intcode.reset()
  return intcode.output[-1]

def teil2(program):
  intcode = Intcode(program)
  x = 0
  for y in range(99,100_000):
    while not inTraktorStrahl(intcode, x, y):
      x += 1
    if inTraktorStrahl(intcode, x+99, y-99):
      return x,y,x*10_000+y-99

x,y,lösung = teil2(program)


print(f'Lösung = {lösung} auf Position {x,y} in {time.perf_counter()-start} Sek.')
