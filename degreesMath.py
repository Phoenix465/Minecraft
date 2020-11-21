"""
Custom Math Class that uses Degrees instead of Radians

"""

from math import sin as oSin
from math import cos as oCos
from math import cos as oTan
from math import pi


def sin(angle: float):
    return oSin(angle * pi / 180)


def cos(angle: float):
    return oCos(angle * pi / 180)


def tan(angle: float):
    return oTan(angle * pi / 180)


def average(*args):
    return sum(args) / len(args)
