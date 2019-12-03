lösung = 0
with open("tag2.txt") as f:
  text = f.readline()
  aufgabe = text.split(",")
  aufgabe = [int(x) for x in aufgabe]

temp_aufgabe = aufgabe.copy()

  
for aufg1 in range(100):
  for aufg2 in range(100):
    position = 0  
    aufgabe = temp_aufgabe.copy()
    aufgabe[1] = aufg1
    aufgabe[2] = aufg2
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
    if aufgabe[0] == 19690720:
      print(aufgabe[0],aufg1, aufg2)