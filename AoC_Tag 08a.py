import time
import itertools
time_start = time.perf_counter()

with open('Tag08.txt') as f:
  puzzle_input = list(map(int,f.readline()))

picture_breite = 25
picture_länge = 25 * 6 #25 pixels wide and 6 pixels tall

pictures = []

for i in range(0,len(puzzle_input),picture_länge):
  picture = puzzle_input[i:i+picture_länge]
  pictures.append(picture)


ziel_picture = []
for position in range(picture_länge):
  for picture in pictures:
    if picture[position] == 2: continue
    ziel_picture.append(picture[position])
    break

for i,pixel in enumerate(ziel_picture):
  if pixel == 0:
    print(' ',end='')
  elif pixel == 1:
    print('X',end='')
  elif pixel == 2:
    print(' ',end='')  
  if (i+1) % picture_breite == 0: print()
print(time.perf_counter() - time_start)

