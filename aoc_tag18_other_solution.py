import collections
import time

time_start = time.perf_counter()

def reachablekeys(start, havekeys):
  bfs = collections.deque([start])
  visited = {start: 0}
  keys = {}
  while bfs:
    h = bfs.popleft()
    for pt in [
        (h[0] + 1, h[1]),
        (h[0] - 1, h[1]),
        (h[0], h[1] + 1),
        (h[0], h[1] - 1),
    ]:
      ch = grid[pt[0]][pt[1]]
      if ch == '#':
        continue
      if pt in visited:
        continue
      visited[pt] = visited[h] + 1
      if ch.isupper() and ch.lower() not in havekeys:
        continue
      if ch.islower() and ch not in havekeys:
        keys[ch] = visited[pt], pt
      else:
        bfs.append(pt)
  return keys


seen = {}
def minwalk(start, havekeys):
  hks = ''.join(sorted(havekeys))
  if (start, hks) in seen:
    return seen[start, hks]
  keys = reachablekeys(start, havekeys)
  if not keys:
    # done!
    ans = 0
  else:
    poss = []
    for ch, (dist, pt) in keys.items():
      #print(start, ch, havekeys, dist)
      poss.append(dist + minwalk(pt, havekeys + ch))
    ans = min(poss)
  seen[start, hks] = ans
  return ans


with open('tag18.txt') as f:
  grid = [l.rstrip('\n') for l in f]
  for i in range(len(grid)):
    for j in range(len(grid[0])):
      if grid[i][j] == '@':
        start = (i, j)

print(minwalk(start, ''), time.perf_counter()-time_start)

