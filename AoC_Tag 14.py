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
überschüssig = defaultdict(int)
def solve(element, needed_amount):
  if element not in elements:
    return
  bekomme = elements[element]['units']
  for e,a in elements[element]['component'].items():
    if e == 'ORE':
      print(f'benötigt von {e} = {needed_amount}, erhalte {bekomme}')
      print(a * math.ceil(needed_amount/bekomme))
      print(a * (needed_amount / bekomme))
      überschüssig[element] += (a * math.ceil(needed_amount/bekomme))-(a * (needed_amount / bekomme))
    a *= math.ceil(needed_amount / bekomme)
    einkaufsliste[e] += a
    solve(e,a)
  return

solve('FUEL',1)
lösung = 0


lösung = einkaufsliste['ORE']
for e,a in überschüssig.items():
  diff = a // elements[e]['units'] * elements[e]['units']
  print(f'Ore reduziert um {diff} wg. überschüssige {e} {a}')
  lösung -= diff

  
print(f'Lösung = {lösung:>9} ORE')
print(f'Lösung - korrektur = {lösung - überschüssig["ORE"]}')
print(einkaufsliste)
print(überschüssig)

