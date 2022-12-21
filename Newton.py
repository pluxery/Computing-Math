import numpy as np
import math as m
from sympy import *

from MathFun import MathFun as mf


class Newton:
    def __init__(self, x, f):
        self.__x = x
        self.__y = [f.subs(Symbol('x'), x) for x in x]
        self.__size = len(x)
        self.__f = f

    def computeRemainder(self, value):
        def getPolynom(value):
            polynom = 1
            for i in range(self.__size):
                if value != self.__x[i]:
                    polynom *= (value - self.__x[i])
            return polynom

        diffFun = mf.derivative(self.__f, self.__size + 1)
        remainder = (diffFun / m.factorial(self.__size + 1)) * getPolynom(value)
        return remainder.subs(Symbol('x'), value)

    @staticmethod
    def dividedDifference(x, y):
        if len(x) > 2:
            xLeft = x[:len(x) - 1]
            xRight = x[1:]
            yLeft = y[:len(x) - 1]
            yRight = y[1:]
            return Newton.dividedDifference(xRight, yRight) - Newton.dividedDifference(xLeft, yLeft)
        if len(x) == 2:
            return expand((y[1] - y[0]) / (x[1] - x[0]))
        raise IndexError(f'check index, dude... :-> {len(x)}')

    @property
    def maxRemainder(self):
        return max([self.computeRemainder(x) for x in self.__x])

    @property
    def minRemainder(self):
        return min([self.computeRemainder(x) for x in self.__x])

    def __divDiffByY(self, idx, n):
        if n == 1:
            return self.__x[idx + 1] - self.__x[idx]
        return self.__divDiffByY(idx + 1, n - 1) - self.__divDiffByY(idx, n - 1)

    def interpolate(self, xValue):

        def firstNewtonsFormula(value):
            def getPolynom(value, size):
                polynom = 1
                for j in range(size):
                    polynom *= (value - self.__x[j])
                return polynom

            result = self.__y[0]
            step = self.__x[1] - self.__x[0]
            for i in range(1, self.__size):
                result += self.__divDiffByY(0, i) / m.factorial(i) * step ** i * getPolynom(value,
                                                                                                       i)
            return result

        def secondNewtonsFormula(value):
            def getPolynom(value, j, size):
                polynom = 1
                for j in range(size):
                    polynom *= (value - self.__x[j])
                    j -= 1
                return polynom

            result = self.__y[-1]
            step = self.__x[1] - self.__x[0]
            n = self.__size - 1
            for i in range(1, self.__size):
                result += self.__divDiffByY(n - 1, i) / m.factorial(i) * step ** i * getPolynom(
                    value, n, i)
                n -= 1
            return result

        def fuckingBessel(value):
            def getPolynom(value, size):
                if size == 0:
                    return 0
                polynom = value
                for i in range(1, size // 2 + 1):
                    polynom *= (value - i)
                for i in range(1, size // 2):
                    polynom *= (value + i)
                return polynom

            def createDivDiffTable():
                table = [[0 for _ in range(self.__size)] for _ in range(self.__size)]
                for i in range(1, self.__size):
                    for j in range(self.__size - i):
                        table[i][j] = table[j + 1][i - 1] - table[j][i - 1]
                for t, y in zip(table, self.__y):
                    t[0] = y
                return table

            yTable = createDivDiffTable()
            half = self.__size // 2
            result = (yTable[half - 1][0] + yTable[half][0]) / 2
            j = half - 1 if self.__size % 2 else half
            xVal = (value - self.__x[j]) / (self.__x[1] - self.__x[0])
            for i in range(1, self.__size):
                if i % 2:
                    result += (xVal - (1 / 2) * getPolynom(xVal, i - 1) * yTable[j][i]) / m.factorial(i)
                else:
                    result += (
                            getPolynom(xVal, i) * (yTable[j][i] + yTable[j - 1][i]) / (m.factorial(i) * 2))
                    j -= 1
            return result

        distanceToBegin = xValue - self.__x[0]
        distanceToMid = abs(xValue - self.__x[self.__size // 2])
        distanceToEnd = self.__x[-1] - xValue
        minDistance = min([distanceToBegin, distanceToMid, distanceToEnd])

        interpolatedValue = 0
        if minDistance == distanceToBegin:
            interpolatedValue = firstNewtonsFormula(xValue)
        elif minDistance == distanceToMid:
            interpolatedValue = fuckingBessel(xValue)
        elif minDistance == distanceToEnd:
            interpolatedValue = secondNewtonsFormula(xValue)
        return expand(interpolatedValue)

