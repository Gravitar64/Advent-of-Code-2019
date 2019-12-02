lösung = 0
with open("tag2.txt") as f:
  text = f.readline()
  aufgabe = text.split(",")
  aufgabe = [int(x) for x in aufgabe]

aufgabe[1] = 12
aufgabe[2] = 2

position = 0    
while True:
  if aufgabe[position] == 99:
    break
  if aufgabe[position] == 1:
    a = aufgabe[position+1]
    b = aufgabe[position+2]
    c = aufgabe[position+3]
    a_wert = aufgabe[a]
    b_wert = aufgabe[b]
    aufgabe[c] = a_wert+b_wert
    position += 4
  if aufgabe[position] == 2:
    a = aufgabe[position+1]
    b = aufgabe[position+2]
    c = aufgabe[position+3]
    a_wert = aufgabe[a]
    b_wert = aufgabe[b]
    aufgabe[c] = a_wert*b_wert
    position += 4
print(aufgabe[0])      