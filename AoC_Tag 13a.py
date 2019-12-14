# Code original by https://www.reddit.com/user/FogleMonster/
# https://www.reddit.com/r/adventofcode/comments/e85b6d/2019_day_9_solutions/faajddr/?context=3

from collections import defaultdict, Counter
from Vector import Vec
import time

class State:
  def __init__(self, program):
    self.mem = defaultdict(int, enumerate(program))
    self.ip = 0
    self.rb = 0
    

start = time.perf_counter()

with open('Tag13.txt') as f:
  program = list(map(int, f.readline().split(',')))

#set quarter input to free play
program[0] = 2

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

def get_sequenz(s,input):
  sequenz = []
  for _ in range(3):
    output = run(s,input)
    if output == None:
      return
    sequenz.append(output)
  return sequenz    

s = State(program)
program_input = paddle_pos = ball_pos = 0
while True:
  sequenz = get_sequenz(s, program_input)
  if sequenz == None: break
  x,y,id = sequenz
  if x == -1 and y == 0:
    lösung = id
  if id == 3:
    paddle_pos = x
  if id == 4:
    ball_pos = x
  if ball_pos > paddle_pos:
    program_input = 1
  if ball_pos < paddle_pos:
    program_input = -1
  if ball_pos == paddle_pos:
    program_input = 0    



print(f'Lösung = {lösung} in {time.perf_counter()-start} Sek.')


