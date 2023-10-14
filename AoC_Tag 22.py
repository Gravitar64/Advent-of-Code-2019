import time
import re


def load(file):
  with open(file) as f:
    return f.read().split('\n')


def solve(p, amount, c):
  for zeile in p:
    n = re.search('-?\d+', zeile)
    if n: n = int(n.group())
    if zeile.startswith('deal into new'): c = (-c - 1) % amount
    elif zeile.startswith('cut'): c = (c - n) % amount
    elif zeile.startswith('deal with'): c = (c * n) % amount
  return c


def polypow(a, b, m, n):
  if not m: return 1, 0
  if not m % 2: return polypow(a * a % n, (a * b + b) % n, m // 2, n)
  else:
    c, d = polypow(a, b, m - 1, n)
    return a * c % n, (a * d + b) % n


def parse(L, puzzle):
  a, b = 1, 0
  for s in reversed(puzzle):
    n = re.search('-?\d+', s)
    if n: n = int(n.group())
    if s == 'deal into new stack':
      a = -a
      b = L - b - 1
    elif s.startswith('cut'):
      b = (b + n) % L
    elif s.startswith('deal with increment'):
      z = pow(n, L - 2, L)  # == modinv(n,L)
      a = a * z % L
      b = b * z % L
  return a, b


def solve2(p, L, N, pos):
    a,b = parse(L,p)
    a,b = polypow(a,b,N,L)
    return (pos*a+b)%L


start = time.perf_counter()
puzzle = load('tag22.txt')
print(f'Part 1: {solve(puzzle,10_007, 2019)}')
print(f'Part 2: {solve2(puzzle,119315717514047, 101741582076661, 2020)}')
print(f'Ermittelt in {time.perf_counter()-start:.5f} Sek.')
