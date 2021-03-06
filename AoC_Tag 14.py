from collections import defaultdict
import math

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

def solve(reactions):
  required = defaultdict(int)
  required['FUEL'] = 1
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

print(f'Lösung = {solve(reactions)}')

