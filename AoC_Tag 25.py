import time
import re
import itertools
from AoC_Intcode import Intcode 


def load(file):
  with open(file) as f:
    return list(map(int, f.read().split(',')))
  

def take_item(item):
  send_input(f'take {item}')
  return {item}  


def drop_item(item):
  send_input(f'drop {item}')
  return {item}


def goto(door):
  INTCODE.output = []
  send_input(door)


def send_input(msg):
  INTCODE.input.extend([ord(c) for c in msg+'\n'])


def ascii2txt():
  return ''.join(chr(n) for n in INTCODE.output)


def parse():
  status = ascii2txt()
  if (room := re.findall('== ([\w ]+) ==',status)): 
    room = room[0]
  if (item := re.findall('Items here:\n- ([\w \n-]+)\n\n',status)):
    item = item[0] 
  if (doors := re.findall('Doors here lead:\n- ([\w \n-]+)\n\n',status)): 
    doors = set(doors[0].split('\n- '))
  return room, item, doors  


def crawl_rooms(target=None):
  seen,inventory = set(), set()
  INTCODE.run()
  room, _, doors = parse()
  queue = [(room,door) for door in doors]
  
  while queue:
    room, door = queue.pop()
    seen.add(room)
    goto(door)
    INTCODE.run()
    room2, item2, doors2 = parse()
    if target == room2: return {OPP_DIRS[door]}
    if item2 and item2 not in TOXIC: inventory |= take_item(item2)
    if room2 in seen: continue
    queue.append((room2,OPP_DIRS[door]))
    for door2 in (doors2-{OPP_DIRS[door]}):
      queue.append((room2,door2))
  return inventory   


def bruteForceCombinations(inventory,door):
  # identify those items, wich are as single item heavier as an android
  all_items = inventory.copy()
  for item in all_items: 
    drop_item(item)
  for item in inventory:
    take_item(item)
    goto(door)
    INTCODE.run()
    if 'lighter' in ascii2txt(): 
      all_items -= {item}
    drop_item(item)
  inventory = set()    

  #all possible combinations for those items minus too heavy ones
  for n in range(2,len(all_items)+1):
    for combi in itertools.combinations(all_items,n):
      needed = set(combi) - inventory
      not_needed = inventory - set(combi)
      for item in needed: 
        inventory |= take_item(item)
      for item in not_needed:
        inventory -= drop_item(item)
      goto(door)
      if INTCODE.run() == 'terminate': 
        return inventory    


def solve():
  inventory = crawl_rooms(INTCODE)
  noDir = crawl_rooms('Security Checkpoint')
  _,_,doors = parse()
  inventory = bruteForceCombinations(inventory,(doors-noDir).pop())
  print(f'The right inventory items are: {inventory}')
  success_msg = ''.join(chr(n) for n in INTCODE.output).split()[-8]
  return success_msg
  

start = time.perf_counter()
OPP_DIRS = {'north':'south','south':'north','west':'east','east':'west'}
TOXIC = {'photons', 'escape pod', 'molten lava', 'giant electromagnet', 'infinite loop'}
INTCODE = Intcode(load('tag25.txt'))

print(f'Part 1: {solve()}')
print(f'Ermittelt in {time.perf_counter()-start:.5f} Sek.')