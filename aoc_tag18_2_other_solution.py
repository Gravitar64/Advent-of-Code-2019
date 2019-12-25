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

def reachable4(starts, havekeys):
    keys = {}
    for i, start in enumerate(starts):
        for ch, (dist, pt) in reachablekeys(start, havekeys).items():
            keys[ch] = dist, pt, i
    return keys

seen = {}
def minwalk(starts, havekeys):
  hks = ''.join(sorted(havekeys))
  if (starts, hks) in seen:
    return seen[starts, hks]
  keys = reachable4(starts, havekeys)
  if not keys:
    # done!
    ans = 0
  else:
    poss = []
    for ch, (dist, pt, rob_id) in keys.items():
      nstarts = tuple(pt if i == rob_id else p for i, p in enumerate(starts))
      poss.append(dist + minwalk(nstarts, havekeys + ch))
    ans = min(poss)
  seen[starts, hks] = ans
  return ans


with open('tag18_2.txt') as f:
  grid = [l.rstrip('\n') for l in f]
  starts = []
  for i in range(len(grid)):
    for j in range(len(grid[0])):
      if grid[i][j] == '@':
        starts.append((i, j))

print(minwalk(tuple(starts), ''), time.perf_counter()-time_start)

