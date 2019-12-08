from collections import Counter
import time
import itertools
time_start = time.perf_counter()

with open('Tag08.txt') as f:
  puzzle_input = list(map(int,f.readline()))

picture_länge = 25 * 6 #25 pixels wide and 6 pixels tall

pictures = []

for i in range(0,len(puzzle_input),picture_länge):
  picture =Counter(puzzle_input[i:i+picture_länge])
  pictures.append(picture)

best = 999999
for picture in pictures:
  if picture[0] < best:
    best = picture[0]
    best_picture = picture

print(best_picture[1] * best_picture[2])
print(time.perf_counter() - time_start)

