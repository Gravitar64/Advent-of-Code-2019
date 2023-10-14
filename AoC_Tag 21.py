# Intcode Class Code original by https://www.reddit.com/user/FogleMonster/
# https://www.reddit.com/r/adventofcode/comments/e85b6d/2019_day_9_solutions/faajddr/?context=3
from collections import defaultdict
import time


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
      if op == 99: return
      size = [0, 4, 4, 2, 2, 3, 3, 4, 4, 2][op]
      args = [self.mem[self.ip+i] for i in range(1, size)]
      modes = [(self.mem[self.ip] // 10 ** i) % 10 for i in range(2, 5)]
      reads = [(self.mem[x], x, self.mem[x+self.rb])[m] for x, m in zip(args, modes)]
      writes = [(x, None, x+self.rb)[m] for x, m in zip(args, modes)]
      self.ip += size
      if op == 1: self.mem[writes[2]] = reads[0] + reads[1]
      if op == 2: self.mem[writes[2]] = reads[0] * reads[1]
      if op == 3: self.mem[writes[0]] = self.input.pop(0)
      if op == 4: self.output.append(reads[0])
      if op == 5 and reads[0]: self.ip = reads[1]
      if op == 6 and not reads[0]: self.ip = reads[1]
      if op == 7: self.mem[writes[2]] = int(reads[0] < reads[1])
      if op == 8: self.mem[writes[2]] = int(reads[0] == reads[1])
      if op == 9: self.rb += reads[0]


def load(file):
  with open(file) as f:
    return list(map(int, f.read().split(',')))


def generiere_input(part1):
  if part1:
    return "NOT A T\nNOT T T\nAND B T\nAND C T\nNOT T J\nAND D J\nWALK\n"
  else:
    return "NOT A T\nNOT T T\nAND B T\nAND C T\nNOT T J\nAND D J\nNOT H T\nNOT T T\nOR E T\nAND T J\nRUN\n"


def solve(program, part1):
  intcode = Intcode(program)
  intcode.load_input([ord(x) for x in generiere_input(part1)])
  intcode.run()
  return intcode.output[-1]
  

start = time.perf_counter()
program = load('tag21.txt')
print(f'Part 1: {solve(program,True)}')
print(f'Part 2: {solve(program,False)}')
print(f'Ermittelt in {time.perf_counter()-start:.5f} Sek.')
