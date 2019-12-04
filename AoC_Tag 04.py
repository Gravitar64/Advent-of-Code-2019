range_von, range_bis = 357253,892943

lösung = 0
for password in range(range_von, range_bis):
  text = str(password)
  double = False
  for x in range(5):
    if text[x] == text[x+1]:
      double = True
  increasing = True
  for x in range(5):
    if text[x] > text[x+1]:
      increasing = False
  if double and increasing: lösung += 1

print(lösung)


      
