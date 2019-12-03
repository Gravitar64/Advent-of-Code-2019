from Vector import Vec
central_port = Vec(1,1)

directions = {'R': Vec(1,0), 'L': Vec(-1,0), 'U': Vec(0,1), 'D':Vec(0,-1)}
wires = []
with open("tag03.txt") as f:
  for line in f:
    wires.append(line.strip().split(","))

positionen = []
for wire in wires:
  position = central_port
  pos_wire = {}
  count_steps = 0
  for wert in wire:
    dir = wert[0]
    steps = int(wert[1:])
    for i in range(steps):
      count_steps += 1
      position += directions[dir]
      pos_wire[position]=count_steps
  positionen.append(pos_wire)

wire1 = {x for x in positionen[0]}
wire2 = {x for x in positionen[1]}
kreuzungen = wire1.intersection(wire2)

min_steps = 99999999
for kreuzung in kreuzungen:
  steps = positionen[0][kreuzung] + positionen[1][kreuzung]
  min_steps = min(min_steps, steps)

print(min_steps)


      
