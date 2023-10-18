import time
from collections import Counter


def load(file):
  with open(file) as f:
    return {(x, y) for y, row in enumerate(f.readlines()) for x, c in enumerate(row) if c == '#'}


def adjacent(x, y):
  for nx, ny in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
    if nx >= 0 and nx < 5 and ny >= 0 and ny < 5:
      yield (nx, ny)


def next_gen(p):
  neighb = Counter([pos for cell in p for pos in adjacent(*cell)])
  return {pos for pos, anz in neighb.items() if anz == 1 and pos in p or
          anz in {1,2} and pos not in p}


def solve(p):
  layouts = {frozenset(p)}
  while True:
    p = next_gen(p)
    if p in layouts:
      break
    layouts.add(frozenset(p))
  return sum([2**(y * 5 + x) for x, y in p])


start = time.perf_counter()
puzzle = load('tag24.txt')
print(f'Part 1: {solve(puzzle)}')

grid = 0
with open("tag24.txt") as f:
    i = 0
    for line in f:
        for c in line.strip():
            if c == "#":
                grid += 1 << i
            i += 1

levels = [0, 0, grid, 0, 0]
for _ in range(200):
    new_levels = [0, 0]

    for j, grid in enumerate(levels[1:-1]):
        new_grid = 0

        for i in range(25):
            if i == 12:
                continue

            count = 0

            if i == 17:
                prev = levels[j + 2] >> 20
                while prev:
                    count += prev & 1
                    prev >>= 1
            elif i >= 5:
                count += (grid >> (i - 5)) & 1
            else:
                count += (levels[j] >> 7) & 1

            if i == 7:
                prev = levels[j + 2] & 31
                while prev:
                    count += prev & 1
                    prev >>= 1
            elif i < 20:
                count += (grid >> (i + 5)) & 1
            else:
                count += (levels[j] >> 17) & 1

            if i == 13:
                for k in range(4, 25, 5):
                    count += (levels[j + 2] >> k) & 1
            elif i % 5:
                count += (grid >> (i - 1)) & 1
            else:
                count += (levels[j] >> 11) & 1

            if i == 11:
                for k in range(0, 25, 5):
                    count += (levels[j + 2] >> k) & 1
            elif i % 5 != 4:
                count += (grid >> (i + 1)) & 1
            else:
                count += (levels[j] >> 13) & 1

            if count == 1 or (count == 2 and not ((grid >> i) & 1)):
                new_grid |= 1 << i

        new_levels.append(new_grid)

    new_levels.extend([0, 0])
    levels = new_levels

res = 0
for grid in levels:
    while grid:
        res += grid & 1
        grid >>= 1

print(res)


print(f'Ermittelt in {time.perf_counter()-start:.5f} Sek.')