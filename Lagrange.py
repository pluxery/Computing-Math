from sympy import *
import numpy as np


class Lagrange:
    def __init__(self, xPoints, function):
        self.__xPoints = xPoints
        self.__function = function
        self.__size = len(xPoints)
        self.__yPoints = [self.__function.subs(Symbol('x'), x) for x in self.__xPoints]

    @property
    def polynomLagrange(self):
        def P(x):
            polynom = 1
            for i in range(self.__size):
                for j in range(self.__size):
                    if i != j:
                        polynom *= (x - self.__xPoints[j]) / (self.__xPoints[i] - self.__xPoints[j])
            return polynom
        return sum([y * P(x) for x, y in zip(self.__xPoints, self.__yPoints)])

    @property
    def __diffFun(self):
        diffFun = self.__function
        for _ in range(self.__size + 1):
            diffFun = diff(diffFun, Symbol('x'))
        return diffFun

    @property
    def absoluteError(self):
        return max([abs(self.polynomLagrange - y) for y in self.__yPoints])

    @property
    def relativeError(self):
        return self.absoluteError / max([abs(y) for y in self.__yPoints])

    @property
    def remainder(self):
        maxValue = max([self.__diffFun.subs(Symbol('x'), x) for x in self.__xPoints])
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
