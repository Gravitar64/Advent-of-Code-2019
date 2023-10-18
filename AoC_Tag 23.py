#Solution by https://www.reddit.com/user/hrunt/

import time


class IntCode:
  def __init__(self, codes):
    self.code = {i: x for i, x in enumerate(codes)}
    self.ptr = 0
    self.relative_base = 0
    self.modes = [0, 0, 0]
    self.inputs = []
    self.outputs = []


  # Comparison functions
  # All IntCode instances are created equal
  def __eq__(self, other):
    return True
  def __ne__(self, other):
    return False
  def __lt__(self, other):
    return False
  def __le__(self, other):
    return True
  def __gt__(self, other):
    return False
  def __ge__(self, other):
    return True


  def inspect(self, pos):
    return self.code[pos]


  def edit(self, pos, val):
    self.code[pos] = val
    return self


  def write(self, input):
    self.inputs.append(input)
    return self


  def read(self):
    return self.outputs.pop(0)


  def run(self):
    res = R_OK
    while res == R_OK:
      res = self._step()
    return res


  def copy(self):
    new = IntCode([])

    new.code = self.code.copy()
    new.ptr = self.ptr
    new.relative_base = self.relative_base
    new.inputs = self.inputs.copy()
    new.outputs = self.outputs.copy()

    return new


  def _step(self):
    mode, op = divmod(self.code.get(self.ptr, 0), 100)
    self.ptr += 1
    self.modes = [int(x) for x in reversed(str(mode))] + [0, 0, 0]

    # opcode 1: add(arg1, arg2) -> arg3
    if op == 1:
      res = self._add()

    # opcode 2: multiply(arg1, arg2) -> arg2
    elif op == 2:
      res = self._mul()

    # opcode 3: read(input) -> arg1
    elif op == 3:
      res = self._read()

    # opcode 4: write(arg1) -> output
    elif op == 4:
      res = self._write()

    # opcode 5: if(arg1) -> jump(arg2)
    elif op == 5:
      res = self._jmp_if_true()

    # opcode 6: if(!arg1) -> jump(arg2)
    elif op == 6:
      res = self._jmp_if_false()

    # opcode 7: ifless(arg1, arg2) -> arg3
    elif op == 7:
      res = self._set_if_lt()

    # opcode 8: ifequal(arg1, arg2) -> arg3
    elif op == 8:
      res = self._set_if_eq()

    # opcode 9: base(arg1) -> relative_base
    elif op == 9:
      res = self._set_base()

    # opcode 99: halt
    elif op == 99:
      res = R_HALT

    # unknown opcode
    else:
      print(f"Invalid opcode {op}")
      res = R_INVALID

    return res


  def _next_value(self):
    return self._next_instr() if self.modes[0] == 1 else self.code.get(self._next_instr(), 0)

  
  def _next_instr(self):
    instr = self.code.get(self.ptr, 0)
    if self.modes.pop(0) == 2:
      instr += self.relative_base
    self.ptr += 1
    return instr


  def _jmp(self, pos):
    self.ptr = pos


  def _add(self):
    arg1 = self._next_value()
    arg2 = self._next_value()
    pos = self._next_instr()

    self.code[pos] = arg1 + arg2
    return R_OK


  def _mul(self):
    arg1 = self._next_value()
    arg2 = self._next_value()
    pos = self._next_instr()

    self.code[pos] = arg1 * arg2
    return R_OK


  def _read(self):
    if len(self.inputs) == 0:
      self.ptr -= 1
      return R_INPUT

    pos = self._next_instr()
    self.code[pos] = self.inputs.pop(0)
    return R_OK


  def _write(self):
    val = self._next_value()
    self.outputs.append(val)
    return R_OUTPUT


  def _jmp_if_true(self):
    val = self._next_value()
    pos = self._next_value()

    if val != 0:
      self._jmp(pos);

    return R_OK


  def _jmp_if_false(self):
    val = self._next_value()
    pos = self._next_value()

    if val == 0:
      self._jmp(pos);

    return R_OK


  def _set_if_lt(self):
    arg1 = self._next_value()
    arg2 = self._next_value()
    pos = self._next_instr()

    self.code[pos] = 1 if arg1 < arg2 else 0
    return R_OK


  def _set_if_eq(self):
    arg1 = self._next_value()
    arg2 = self._next_value()
    pos = self._next_instr()

    self.code[pos] = 1 if arg1 == arg2 else 0
    return R_OK


  def _set_base(self):
    self.relative_base += self._next_value()
    return R_OK


def run_network(codes, address=None):
  computers = {}
  q = {}

  initialized = set()
  active = set()
  idle = set()

  nat = (None, None)
  nat_sent_y = None

  for i in range(50):
    computers[i] = IntCode(codes)
    q[i] = []
    active.add(i)

  run = True
  x, y = None, None

  while run:

    # start off ssuming all nodes are idle
    all_idle = True

    for i, c in computers.items():

      # this node has halted (probably a bug)
      if i not in active:
        continue

      res = c.run()

      if res == R_HALT:
        active -= {i}
        break

      elif res == R_INPUT:

        # first read request is for initialization
        if i not in initialized:
          initialized.add(i)
          c.write(i)

          idle.discard(i)
          all_idle = False

        # send something from the queue if it's available
        elif len(q[i]):
          x, y = q[i].pop(0)
          c.write(x)
          c.write(y)

          idle.discard(i)
          all_idle = False

        # send the idle packet
        # two idle packets in a row means this node is idle
        else:
          c.write(-1)
          if i not in idle:
            idle.add(i)
            all_idle = False

      elif res == R_OUTPUT:

        # if this node sends a packet, it is not idle
        idle.discard(i)
        all_idle = False

        # read the packet (three reads)
        dest = c.read()
        _ = c.run()
        x = c.read()
        _ = c.run()
        y = c.read()

        # if the destination is available, queue it up
        if dest in q:
          q[dest].append((x, y))

        # store the NAT packet
        else:
          if address is not None and address == dest:
            run = False
            break

          if dest == 255:
            nat = (x, y)

      # this node hit a bug
      elif res == R_INVALID:
        print(f"Computer {i} error @ {c.ptr}: {','.join(str(x) for x in c.code)}")
        run = False
        break

    # all systems are idle
    # send a packet to queue 0 from the NAT
    if all_idle:
      nx, ny = nat

      # processing is complete if a NAT Y address repeats
      if nat_sent_y is not None and nat_sent_y == ny:
        x, y = nx, ny
        run = False

      # send the last NAT packet to node 0
      else:
        nat_sent_y = ny
        q[0].append((nx, ny))

  return (x, y)


def run():
  program = open('tag23.txt').read().strip()
  codes = [int(x) for x in program.split(",")]

  x, y = run_network(codes, 255)
  print(f"Packet at address 255: {(x, y)}")

  _, y = run_network(codes)
  print(f"First resent NAT Y address {y}")


R_OK = 0
R_HALT = 1
R_INPUT = 2
R_OUTPUT = 3
R_INVALID = 99
run()