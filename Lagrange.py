from sympy import *
import numpy as np
from MathFun import MathFun as mf


class Lagrange:
    def __init__(self, xPoints, function):
        self.__xPoints = xPoints
        self.__function = function
        self.__size = len(xPoints)
        self.__yPoints = [self.__function.subs(Symbol('x'), x) for x in self.__xPoints]

    @property
    def formulaLagrange(self):
        x = Symbol('x')
        step = self.__xPoints[1] - self.__xPoints[0]
        result = 0
        for i in range(self.__size):
            polynom = 1
            for j in range(self.__size):
                if i != j:
                    polynom *= (x - self.__xPoints[j]) / ((i - j) * step)
            result += self.__yPoints[i] * polynom
        return result

    @property
    def polynomLagrange(self):
        return sum([self.formulaLagrange.subs(Symbol('x'), x) for x in self.__xPoints])

    @property
    def absoluteError(self):
        return max([abs(self.polynomLagrange - y) for y in self.__yPoints])

    @property
    def relativeError(self):
        return self.absoluteError / max([abs(y) for y in self.__yPoints])

    @property
    def remainder(self):
        diffFun = mf.derivative(self.__function, self.__size + 1)
        maxValue = max([abs(diffFun.subs(Symbol('x'), x)) for x in self.__xPoints])
        distance = self.__xPoints[-1] - self.__xPoints[0]
        return maxValue / np.math.factorial(self.__size + 1) * distance ** (self.__size + 1)

    @property
    def yPoints(self):
        return self.__yPoints

    @property
    def xPoints(self):
        return self.__xPoints

    def __str__(self):
        return f'n: {self.__size}, ∆fn: {self.absoluteError}, δfn: {self.relativeError}, rn: {self.remainder}'
