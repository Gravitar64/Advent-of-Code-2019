import time
time_start = time.perf_counter_ns()
need = 'acg'
have = 'gfca'
have = ''.join(sorted(list(have)))
print(need in have, time.perf_counter_ns() - time_start)

time_start = time.perf_counter_ns()
have = 'gfca'
print(all([x in have for x in need]), time.perf_counter_ns() - time_start)

time_start = time.perf_counter_ns()
need1 = {'a', 'c', 'g'}
have1 = {'g', 'f', 'c', 'a'}
print (need1.issubset(have1),time.perf_counter_ns() - time_start)

print(hash(frozenset(need1)))
