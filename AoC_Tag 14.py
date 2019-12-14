from collections import defaultdict
import math

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
    elements[output]['component'] = units  


einkaufsliste = defaultdict(int)
def solve(element, needed_amount):
  if element not in elements:
    return
  bekomme = elements[element]['units']
  for e,a in elements[element]['component'].items():
    a *= math.ceil(needed_amount / bekomme)
    if e != 'ORE':
      einkaufsliste[e] += a
    solve(e,a)
  return

solve('FUEL',1)
lösung = 0
for name, needed in einkaufsliste.items():
  if name not in ores: continue
  bekomme, preis = ores[name]
  ore = math.ceil(needed / bekomme) * preis
  lösung += ore
  print(f'Consume {ore:>10} ORE for {needed:>5} {name} ({preis} ORES for {bekomme} {name})')
  
print(f'Lösung = {lösung:>9} ORE')
print(einkaufsliste)

