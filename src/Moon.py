# from https://he.wikipedia.org/wiki/%D7%94%D7%99%D7%A8%D7%97
from Point import *

RADIUS = 3475 * 1000  # meters
ACC = 1.622  # m/s^2
EQ_SPEED = 1700  # m/s

real_dest_point = Point(268467, 0)


def getAcc(speed: float) -> float:
    n = abs(speed) / EQ_SPEED
    return (1 - n) * ACC
