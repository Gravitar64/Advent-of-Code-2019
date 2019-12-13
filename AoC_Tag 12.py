from Vector import Vec 
import re 
import time

start_time = time.perf_counter()

class Moon:
  def __init__(self, pos):
    self.pos = pos
    self.vel = Vec(0,0,0)

puzzle_input = []
with open('Tag12.txt') as f:
  for line in f:
    line = re.sub('[<>x=yz,]','',line)
    line = list(map(int,line.split()))
    puzzle_input.append(Vec(*line))

moons = []
for pos in puzzle_input:
  moons.append(Moon(pos))
for _ in range(1000):
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
   

lösung = 0
for moon in moons:
  pe = sum([abs(x) for x in moon.pos])
  ke = sum([abs(x) for x in moon.vel])
  te = pe * ke
  lösung += te

print(f'Lösung: {lösung} in {time.perf_counter() - start_time} Sek.') 