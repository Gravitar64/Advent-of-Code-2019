from collections import defaultdict
import math
import time

time_start = time.perf_counter()

reactions = defaultdict(dict)
with open('tag14.txt') as f:
  for line in f:
    inputs, outputs = line.strip().split('=>')
    inputs = inputs.split(',')
    unit, chemical = outputs.split()
    reactions[chemical] = {'name': chemical, 'units': int(unit)}
    components = {}
    for input in inputs:
      u,c = input.split()
      components[c] = int(u)
    reactions[chemical]['components'] = components

def solve(reactions, fuel):
  required = defaultdict(int)
  required['FUEL'] = fuel
  stack = [reactions['FUEL']]
  while stack:
    reaction = stack.pop()
    multi = math.ceil(required[reaction['name']] / reaction['units'])
    for component, units in reaction['components'].items():
      required[component] += units * multi
      if component in reactions:
        stack.append(reactions[component])
    required[reaction['name']] -= reaction['units'] * multi
  return required['ORE']

def solve2(guess):
  step = 500000
  fertig = False
  low = True
  ore = 0
  while step > 0.5:
    ore = solve(reactions, guess)
    if ore < 1_000_000_000_000:
      guess += step
      if not low:
        low = True
        step /= 2
    else:
      guess -= step
      if low:
        low = False
        step /= 2
  return int(guess)

print(f'Lösung = {solve2(1102168)} in {time.perf_counter() - time_start} Sek.')

