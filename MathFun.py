from sympy import *


class MathFun:
    __x = Symbol('x')

    @classmethod
    def derivative(cls, function, n):
        derivativeFun = function
        for _ in range(n):
            derivativeFun = diff(derivativeFun, cls.__x)
        return derivativeFun

    @classmethod
    def norm(cls, y: list) -> float:
        return max([abs(yi) for yi in y])

    @classmethod
    def rn(cls, y1: list, y2: list) -> float:
        return cls.norm([abs(s - y) for s, y in zip(y1, y2)])
