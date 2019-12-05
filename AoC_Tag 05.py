input_value = 1

with open("tag05.txt") as f:
  code = list(map(int, f.readline().split(",")))
  

pp = 0
while True:
  instruction = f'{code[pp]:0>5}'
  opcode = int(instruction[-2:])
  modi = [int(instruction[x]) for x in range(3)]  
  if opcode == 99:
    break
  if opcode == 1:
    p1,p2,p3 = code[pp+1:pp+4]
    m3,m2,m1 = modi
    w1 = code[p1] if m1 == 0 else p1
    w2 = code[p2] if m2 == 0 else p2
    code[p3] = w1 + w2 
    pp += 4
  if opcode == 2:
    p1,p2,p3 = code[pp+1:pp+4]
    m3,m2,m1 = modi
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
   