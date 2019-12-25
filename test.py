import time
pferd = 31
ochse = 21

time_start = time.perf_counter()
zielsumme = 1770
counter = 0
for p in range(zielsumme//pferd+1):
  for o in range(zielsumme//ochse+1):
    counter += 1
    if p*pferd + o *ochse == zielsumme:
      print(f'Lösung Nr. {counter}: {p} Pferde + {o} Ochsen kosten {p*pferd} + {o*ochse} = {p*pferd+o*ochse}')
print(f'Untersuchte Varianten = {counter} in {time.perf_counter()-time_start} Sek.')
print()

time_start = time.perf_counter()
zielsumme = 1770
counter = 0
for p in range(zielsumme//pferd+1):
  letzte_ziffer = p % 10
  for o in range(10-letzte_ziffer,zielsumme//ochse+1,10):
    counter += 1
    if p*pferd + o *ochse == zielsumme:
      print(f'Lösung Nr. {counter}: {p} Pferde + {o} Ochsen kosten {p*pferd} + {o*ochse} = {p*pferd+o*ochse}')
print(f'Untersuchte Varianten = {counter} in {time.perf_counter()-time_start} Sek.')
print()


time_start = time.perf_counter()
zielsumme = 177
counter = 0
for p in range(zielsumme//pferd+1):
  for o in range(zielsumme//ochse+1):
    counter += 1
    if p*pferd + o *ochse == zielsumme:
      print(f'Lösung Nr. {counter}: {p} Pferde + {o} Ochsen kosten {p*pferd} + {o*ochse} = {p*pferd+o*ochse}')
print(f'Untersuchte Varianten = {counter} in {time.perf_counter()-time_start} Sek.')
print()

time_start = time.perf_counter()
zielsumme = 177
counter = 0
for p in range(8):
  o = 7-p
  counter += 1
  if p*pferd + o *ochse == zielsumme:
    print(f'Lösung Nr. {counter}: {p} Pferde + {o} Ochsen kosten {p*pferd} + {o*ochse} = {p*pferd+o*ochse}')
print(f'Untersuchte Varianten = {counter} in {time.perf_counter()-time_start} Sek.')
print()