from collections import defaultdict
import time
import itertools
time_start = time.perf_counter()

with open('Tag07.txt') as f:
  code_orig = list(map(int,f.readline().split(',')))
#code_orig = list(map(int,"3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0".split(',')))
print(code_orig)
phase_sequenz = [0,1,2,3,4]

best_soulution = 0
for permutation in itertools.permutations(phase_sequenz):
  for amp_counter in range(5):
    first = True
    pp = 0
    code = code_orig.copy()
    if amp_counter == 0:
      amp_input = 0
    amp_phase = permutation[amp_counter]  
    while True:
      instruction = f'{code[pp]:0>5}'
      opcode = int(instruction[-2:])
      modi = [int(instruction[x]) for x in range(3)]  
      m3,m2,m1 = modi
      if opcode == 99:
        break
      if opcode == 1:
        p1,p2,p3 = code[pp+1:pp+4]
        w1 = code[p1] if m1 == 0 else p1
        w2 = code[p2] if m2 == 0 else p2
        code[p3] = w1 + w2 
        pp += 4
      if opcode == 2:
        p1,p2,p3 = code[pp+1:pp+4]
        w1 = code[p1] if m1 == 0 else p1
        w2 = code[p2] if m2 == 0 else p2
        code[p3] = w1 * w2
        pp += 4
      if opcode == 3:
        p1 = code[pp+1]
        if first:
          code[p1] = amp_phase
          first = False
        else:
          code[p1] = amp_input  
        pp += 2
      if opcode == 4:
        p1 = code[pp+1]
        if amp_counter == 4:
          best_soulution = max(best_soulution, code[p1])
        amp_input = code[p1]
        
        pp += 2 
      if opcode == 5:
        p1, p2 = code[pp+1:pp+3]
        w1 = code[p1] if m1 == 0 else p1
        w2 = code[p2] if m2 == 0 else p2
        if w1 != 0:
          pp = w2
        else: 
          pp += 3  
      if opcode == 6:
        p1, p2 = code[pp+1:pp+3]
        w1 = code[p1] if m1 == 0 else p1
        w2 = code[p2] if m2 == 0 else p2
        if w1 == 0:
          pp = w2
        else: 
          pp += 3   
      if opcode == 7:
        p1, p2, p3 = code[pp+1:pp+4]
        w1 = code[p1] if m1 == 0 else p1
        w2 = code[p2] if m2 == 0 else p2
        if w1 < w2:
          code[p3] = 1
        else:
          code[p3] = 0
        pp += 4    
      if opcode == 8:
        p1, p2, p3 = code[pp+1:pp+4]
        w1 = code[p1] if m1 == 0 else p1
        w2 = code[p2] if m2 == 0 else p2
        if w1 == w2:
          code[p3] = 1
        else:
          code[p3] = 0
        pp += 4
  
print(best_soulution)  