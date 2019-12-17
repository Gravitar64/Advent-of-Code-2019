import math

class Vec(tuple):
  """Eigene Vektor-Klasse um 2D-nDimensionale Koordinaten zu hinterlegen und zu addieren, subtrahieren, etc."""
  def __new__(cls, *args):
    return tuple.__new__(cls, args)

  def __add__(self, other):
    return Vec(*tuple(a+b for a, b in zip(self, other)))

  def __sub__(self, other):
    return Vec(*tuple(a-b for a, b in zip(self, other)))

  def __mul__(self, faktor):
    return Vec(*tuple(a*faktor for a in self))

  def __truediv__(self, divisor):
    return Vec(*tuple(a / divisor for a in self))

  def abstand(self, other):
    """Liefert den Manhatten-Abstand (https://de.wikipedia.org/wiki/Manhattan-Metrik) zwischen 2 Koordinaten"""
    return sum(abs(a-b) for a, b in zip(self, other))

  def winkel(self, other):
    """Liefert den Winkel in Grad zwischen Vec1 und Vec2. Senkrecht oben ist 0°, die Gradzahl wächst gegen den Uhrzeigersinn"""
    return math.degrees(math.atan2(*(self - other)) % (2 * math.pi))  
  