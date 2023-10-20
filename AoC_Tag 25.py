# Intcode Class Code original by https://www.reddit.com/user/FogleMonster/
# https://www.reddit.com/r/adventofcode/comments/e85b6d/2019_day_9_solutions/faajddr/?context=3
from collections import defaultdict
import time
import re
import itertools


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
      if op == 99: return "terminate"
      size = [0, 4, 4, 2, 2, 3, 3, 4, 4, 2][op]
      args = [self.mem[self.ip+i] for i in range(1, size)]
      modes = [(self.mem[self.ip] // 10 ** i) % 10 for i in range(2, 5)]
      reads = [(self.mem[x], x, self.mem[x+self.rb])[m] for x, m in zip(args, modes)]
      writes = [(x, None, x+self.rb)[m] for x, m in zip(args, modes)]
      self.ip += size
      if op == 1: self.mem[writes[2]] = reads[0] + reads[1]
      if op == 2: self.mem[writes[2]] = reads[0] * reads[1]
      if op == 3: 
        if not self.input:
          return 'wait for input'
        else:
          self.mem[writes[0]] = self.input.pop(0)
      if op == 4: self.output.append(reads[0])
      if op == 5 and reads[0]: self.ip = reads[1]
      if op == 6 and not reads[0]: self.ip = reads[1]
      if op == 7: self.mem[writes[2]] = int(reads[0] < reads[1])
      if op == 8: self.mem[writes[2]] = int(reads[0] == reads[1])
      if op == 9: self.rb += reads[0]


def load(file):
  with open(file) as f:
    return list(map(int, f.read().split(',')))
  

def take_item(item, inventory, toxic, intcode):
  if item in toxic: return inventory
  send_input(f'take {item}',intcode)
  return inventory | {item}  


def drop_item(item, inventory, intcode):
  send_input(f'drop {item}', intcode)
  return inventory - {item}


def send_input(msg,intcode):
  intcode.input.extend([ord(c) for c in msg+'\n'])


def parse(output):
  status = ''.join(chr(n) for n in output)
  if (room := re.findall('== ([\w ]+) ==',status)): 
    room = room[0]
  if (item := re.findall('Items here:\n- ([\w \n-]+)\n\n',status)):
    item = item[0] 
  if (doors := re.findall('Doors here lead:\n- ([\w \n-]+)\n\n',status)): 
    doors = set(doors[0].split('\n- '))
  return room, item, doors  


def crawl_rooms(intcode,target=None):
  revDoor = {'north':'south','south':'north','west':'east','east':'west'}
  toxic_items = {'photons', 'escape pod', 'molten lava', 'giant electromagnet', 'infinite loop'}
  seen,inventory = set(), set()
  intcode.run()
  room, _, doors = parse(intcode.output)
  queue = [(room,door) for door in doors]
  
  while queue:
    room, door = queue.pop()
    seen.add(room)
    send_input(door,intcode)
    intcode.output = []
    intcode.run()
    room2, item2, doors2 = parse(intcode.output)
    if target == room2: return {revDoor[door]}
    if item2: inventory = take_item(item2,inventory,toxic_items,intcode)
    if room2 in seen: continue
    queue.append((room2,revDoor[door]))
    for door2 in (doors2-{revDoor[door]}):
      queue.append((room2,door2))
  return inventory   


def bruteForceCombinations(inventory,door,intcode):
  all_items = inventory.copy()
  for n in range(len(all_items),0,-1):
    for combi in itertools.combinations(all_items,n):
      needed = set(combi) - inventory
      not_needed = inventory - set(combi)
      inventory = (inventory - not_needed) | needed
      for item in needed: 
        send_input(f'take {item}',intcode)
      for item in not_needed:
        send_input(f'drop {item}',intcode)
      intcode.run()
      intcode.output = []
      send_input(door,intcode)
      if intcode.run() == 'terminate': return inventory


def solve(program):
  intcode = Intcode(program)
  inventory = crawl_rooms(intcode)
  noDir = crawl_rooms(intcode,'Security Checkpoint')
  _,_,doors = parse(intcode.output)
  inventory = bruteForceCombinations(inventory,(doors-noDir).pop(), intcode)
  print(f'The right inventory items are: {inventory}')
  success_msg = ''.join(chr(n) for n in intcode.output).split()[-8]
  return success_msg
  

start = time.perf_counter()
program = load('tag25.txt')
print(f'Part 1: {solve(program)}')
print(f'Ermittelt in {time.perf_counter()-start:.5f} Sek.')
