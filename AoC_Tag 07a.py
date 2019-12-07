from collections import defaultdict
import time
import itertools
time_start = time.perf_counter()

with open('Tag07.txt') as f:
  prog_orig = list(map(int,f.readline().split(',')))
#prog_orig = list(map(int,"3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10".split(',')))
phase_sequenz = [9,8,7,6,5]
best_solution = 0

class Amp:
  def __init__(self,prog,phase):
    self.prog = prog.copy()
    self.phase = phase
    self.phase_first = True
    self.output = 0
    self.halt = False
    self.pp = 0

def run_amp(amp,phase,input):
  while amp.prog[amp.pp] != 99:
    instruction = f'{amp.prog[amp.pp]:0>5}'
    opcode = int(instruction[-2:])
    modi = [int(instruction[x]) for x in range(3)]  
    m3,m2,m1 = modi
    if opcode == 1:
      p1,p2,p3 = amp.prog[amp.pp+1:amp.pp+4]
      w1 = amp.prog[p1] if m1 == 0 else p1
      w2 = amp.prog[p2] if m2 == 0 else p2
      amp.prog[p3] = w1 + w2 
      amp.pp += 4
    if opcode == 2:
      p1,p2,p3 = amp.prog[amp.pp+1:amp.pp+4]
      w1 = amp.prog[p1] if m1 == 0 else p1
      w2 = amp.prog[p2] if m2 == 0 else p2
      amp.prog[p3] = w1 * w2
      amp.pp+= 4
    if opcode == 3:
      p1 = amp.prog[amp.pp+1]
      if amp.phase_first:
        amp.prog[p1] = phase
        amp.phase_first = False
      else:
        amp.prog[p1] = input 
      amp.pp+= 2
    if opcode == 4:
      p1 = amp.prog[amp.pp+1]
      amp.output = amp.prog[p1]
      amp.pp += 2
      return
    if opcode == 5:
      p1, p2 = amp.prog[amp.pp+1:amp.pp+3]
      w1 = amp.prog[p1] if m1 == 0 else p1
      w2 = amp.prog[p2] if m2 == 0 else p2
      if w1 != 0:
        amp.pp= w2
      else: 
        amp.pp+= 3  
    if opcode == 6:
      p1, p2 = amp.prog[amp.pp+1:amp.pp+3]
      w1 = amp.prog[p1] if m1 == 0 else p1
      w2 = amp.prog[p2] if m2 == 0 else p2
      if w1 == 0:
        amp.pp = w2
      else: 
        amp.pp += 3   
    if opcode == 7:
      p1, p2, p3 = amp.prog[amp.pp+1:amp.pp+4]
      w1 = amp.prog[p1] if m1 == 0 else p1
      w2 = amp.prog[p2] if m2 == 0 else p2
      if w1 < w2:
        amp.prog[p3] = 1
      else:
        amp.prog[p3] = 0
      amp.pp+= 4    
    if opcode == 8:
      p1, p2, p3 = amp.prog[amp.pp+1:amp.pp+4]
      w1 = amp.prog[p1] if m1 == 0 else p1
      w2 = amp.prog[p2] if m2 == 0 else p2
      if w1 == w2:
        amp.prog[p3] = 1
      else:
        amp.prog[p3] = 0
      amp.pp+= 4
  amp.halt = True

for permutation in itertools.permutations(phase_sequenz):
  amps = [Amp(prog_orig,permutation[x]) for x in range(5)]
  active = 0
  while not amps[4].halt:
    run_amp(amps[active], amps[active].phase, amps[active-1].output)
    active = (active +1) % 5
  best_solution = max(best_solution, amps[4].output)    
  
print(best_solution)
print(time.perf_counter() - time_start)  