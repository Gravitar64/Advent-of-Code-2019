lösung = 0
with open("tag1.txt") as f:
  for masse in f:
    masse = int(masse)
    treibstoff = masse // 3 - 2
    zusatztreibstoff = 0
    zusatz = treibstoff
    while True:
      zusatz = zusatz // 3 - 2
      if zusatz <= 0:
        break
      zusatztreibstoff += zusatz
    lösung = lösung + treibstoff + zusatztreibstoff  
print (lösung)    