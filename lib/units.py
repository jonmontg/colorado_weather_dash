
# ===========
# temperature
# ===========

def c_to_f(c):
  return c * 9/5 + 32

def f_to_c(f):
  return (f - 32) * 5/9

def temp_units(units):
  if units == "us":
    return "F"
  else:
    return "C"

def convert_temp(x, inp, out):
  if inp == out:
    return x
  if inp == "us":
    return f_to_c(x)
  return c_to_f(x)

# =====
# Speed
# =====

def mph_to_kph(mph):
  return mph * 1.60934

def kph_to_mph(kph):
  return kph / 1.60934

def speed_units(units):
  if units == "us":
    return "mph"
  else:
    return "km/h"

def convert_speed(x, inp, out):
  if inp == out:
    return x
  if inp == "us":
    return kph_to_mph(x)
  return mph_to_kph(x)