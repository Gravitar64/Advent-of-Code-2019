from Vector import Vec 
import re 
import time
import math

start_time = time.perf_counter()

class Moon:
  def __init__(self, pos):
    self.pos = pos
    self.vel = Vec(0,0,0)

  def state (self,n):
    return self.pos[n], self.vel[n]  

puzzle_input = []
with open('Tag12.txt') as f:
  for line in f:
    line = re.sub('[<>x=yz,]','',line)
    line = list(map(int,line.split()))
    puzzle_input.append(Vec(*line))

moons = []
for pos in puzzle_input:
  moons.append(Moon(pos))
lösungen = []  

for achsen_zähler in range(3):
  moons = []
  for pos in puzzle_input:
    moons.append(Moon(pos))
  start_state = tuple(moon.state(achsen_zähler) for moon in moons)
  fertig = False
  cycles = 0
  while not fertig:
    cycles += 1
    for moon1 in moons:
      for moon2 in moons:
        if moon1 == moon2: continue
        diff = moon2.pos - moon1.pos
        vel_list = list(moon1.vel)
        for i,achse in enumerate(diff):
          if achse == 0: continue
          if achse > 0:
            vel_list[i] += 1
          if achse < 0:
            vel_list[i] -= 1
        moon1.vel = Vec(*vel_list)    
    for moon in moons:
      moon.pos += moon.vel
    state = tuple(moon.state(achsen_zähler) for moon in moons)
    #state = moons[0].state()
    if state == start_state:
      fertig = True
      lösungen.append(cycles)

a,b,c = lösungen

kgv = (a * b) // math.gcd(a,b)
kgv2 = (kgv * c) // math.gcd(kgv,c)
print(f'Lösung: {kgv2} in {time.perf_counter() - start_time} Sek.') 