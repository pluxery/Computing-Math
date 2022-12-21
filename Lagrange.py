from sympy import *
import numpy as np
from MathFun import MathFun as mf


class Lagrange:
    def __init__(self, xPoints, function):
        self.__x = xPoints
        self.__f = function
        self.__size = len(xPoints)
        self.__y = [self.__f.subs(Symbol('x'), x) for x in self.__x]

    @property
    def getFormulaLagrange(self):
        x = Symbol('x')
        step = self.__x[1] - self.__x[0]
        result = 0
        for i in range(self.__size):
            polynom = 1
            for j in range(self.__size):
                if i != j:
                    polynom *= (x - self.__x[j]) / ((i - j) * step)
            result += self.__y[i] * polynom
        return result

    @property
    def polynomLagrange(self):
        return sum([self.getFormulaLagrange.subs(Symbol('x'), x) for x in self.__x])

    @property
    def absoluteError(self):
        return max([abs(self.polynomLagrange - y) for y in self.__y])

    @property
    def relativeError(self):
        return self.absoluteError / max([abs(y) for y in self.__y])

    @property
    def remainder(self):
        diffFun = mf.derivative(self.__f, self.__size + 1)
        maxValue = max([abs(diffFun.subs(Symbol('x'), x)) for x in self.__x])
        distance = self.__x[-1] - self.__x[0]
        return maxValue / np.math.factorial(self.__size + 1) * distance ** (self.__size + 1)

    @property
    def yPoints(self):
        return self.__y

    @property
    def xPoints(self):
        return self.__x

    def __str__(self):
        return f'n: {self.__size}, ∆fn: {self.absoluteError}, δfn: {self.relativeError}, rn: {self.remainder}'
