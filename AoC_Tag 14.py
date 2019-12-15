from collections import defaultdict
import math
import time

time_start = time.perf_counter()

elements = defaultdict(dict)
ores = {}
with open('tag14.txt') as f:
  for line in f:
    input, output = line.strip().split('=>')
    inputs = input.split(',')
    income,output = output.split()
    elements[output] = {'name':output,'units':int(income)}
    units = {}
    for input in inputs:
      u,c = input.split()
      units[c] = int(u)
      if c == 'ORE':
        ores[output] = [int(income), int(u)]
    elements[output]['components'] = units  


def solve_ore(elements, fuel=1):
  required = defaultdict(int)
  required["FUEL"] = fuel
  stack = [elements["FUEL"]]
  
  while len(stack) > 0:
    element = stack.pop()
    needed = math.ceil(required[element["name"]] / element["units"])
    for component, units in element["components"].items():
      required[component] += needed * units
      if component in elements:
        stack.append(elements[component])
    required[element["name"]] -= needed * element["units"]
  return required["ORE"]

  
print(f'Lösung = {solve_ore(elements)} ORE in {time.perf_counter()-time_start} Sek.')


