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
  pos_wire = set()
  for wert in wire:
    dir = wert[0]
    steps = int(wert[1:])
    for i in range(steps):
      position += directions[dir]
      pos_wire.add(position)
  positionen.append(pos_wire)

kreuzungen = positionen[0].intersection(positionen[1])

min_abstand = 99999999
for kreuzung in kreuzungen:
  abst = central_port.abstand(kreuzung)
  min_abstand = min(min_abstand, abst)

print(min_abstand)


      
