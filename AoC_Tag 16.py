from collections import deque
import time

time_start = time.perf_counter()

standard_pattern = [0, 1, 0, -1]
input_signal = 59791911701697178620772166487621926539855976237879300869872931303532122404711706813176657053802481833015214226705058704017099411284046473395211022546662450403964137283487707691563442026697656820695854453826690487611172860358286255850668069507687936410599520475680695180527327076479119764897119494161366645257480353063266653306023935874821274026377407051958316291995144593624792755553923648392169597897222058613725620920233283869036501950753970029182181770358827133737490530431859833065926816798051237510954742209939957376506364926219879150524606056996572743773912030397695613203835011524677640044237824961662635530619875905369208905866913334027160178
signal = [int(a) for a in str(input_signal)]


def generate_pattern(anzahl):
  patterns = {}
  for phase in range(1,anzahl+1):
    pattern = deque()
    for zahl in standard_pattern:
      for i in range(phase):
        pattern.append(zahl)
    pattern.rotate(-1)
    patterns[phase] = pattern
  return patterns


def fft(signal):
  fft = []
  for phase in range(len(signal)):
    summe = 0
    pattern = patterns[phase+1].copy()
    for i in range(len(signal)):
      summe += signal[i] * pattern[0]
      pattern.rotate(-1)
    last_digit = abs(summe) % 10
    fft.append(last_digit)
  return fft 

patterns = generate_pattern(len(signal))
for phase in range(100):
  signal = fft(signal)

print(f'Lösung = {int("".join(map(str,signal[:8])))} in {time.perf_counter() - time_start} Sek')

