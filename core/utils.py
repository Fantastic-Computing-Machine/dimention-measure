import math


def formatFloat(f, n=2):
    return math.floor(f * 10 ** n) / 10 ** n
