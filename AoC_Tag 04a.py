from collections import defaultdict
range_von, range_bis = 357253,892943

lösung = 0
for password in range(range_von, range_bis):
  text = str(password)
  
  increasing = True
  for x in range(5):
    if text[x] > text[x+1]:
      increasing = False
  
  doubles = defaultdict(int)
  
  for x in range(5):
    if text[x] == text[x+1]:
      doubles[text[x]] += 1
  
  double = False
  for passw, anz in doubles.items():
    if anz == 1:
      double = True
      break
  if double and increasing: lösung += 1


print(lösung)


      
