input_value = 5

with open("tag05.txt") as f:
  code = list(map(int, f.readline().split(",")))

#code = list(map(int,"3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99".split(",")))  

pp = 0
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
    code[p1] = input_value
    pp += 2
  if opcode == 4:
    p1 = code[pp+1]
    print(code[p1])
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

# Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
# Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
# Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
# Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.   