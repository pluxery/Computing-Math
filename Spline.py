import math as m
import numpy as np


def f(x: float):
    return x * x - m.sin(m.pi * x)


def df(x: float) -> float:
    return 2 * x - m.cos(m.pi * x) * m.pi


class Spline:
    def __init__(self, n: int, a: float = 0.4, b: float = 0.9):
        self.a = a
        self.b = b
        self.n = n
        self.h = (b - a) / n

    def interpolate(self, x: float) -> float:
        h = self.h

        a = f(x)
        b = df(x)
        c = (12 / h ** 2) * ((df(x) + df(x + h)) / 2 - (f(x + h) - f(x)) / h)
        d = (6 / h) * ((-2 * df(x) + df(x + h)) / 3 + (f(x + h) - f(x)) / h)

        return a + b * h + c * h ** 2 + d * h ** 3

    @property
    def y(self):
        return [f(xi) for xi in self.x]

    @property
    def x(self):
        return np.linspace(self.a, self.b, self.n)
