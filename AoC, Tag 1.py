lösung = 0
with open("tag1.txt") as f:
  for masse in f:
    masse = int(masse)
    lösung += masse // 3 - 2
    
print (lösung)    