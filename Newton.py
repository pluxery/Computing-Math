import numpy as np
import math as m
from sympy import *


class Newton:
    def __init__(self, xPoints, function):
        self.__xPoints = xPoints
        self.__yPoints = [function.subs(Symbol('x'), x) for x in xPoints]
        self.__size = len(xPoints)
        self.__function = function

    def computeRemainder(self, value):
        def getPolynom(value):
            polynom = 1
            for i in range(self.__size):
                if value != self.__xPoints[i]:
                    polynom *= (value - self.__xPoints[i])
            return polynom

        def derivative(function, pow):
            derivativeFun = function
            for _ in range(pow):
                derivativeFun = diff(derivativeFun, Symbol('x'))
            return derivativeFun

        derivativeOfFunction = derivative(self.__function, self.__size + 1)
        remainder = (derivativeOfFunction / m.factorial(self.__size + 1)) * getPolynom(value)
        return remainder.subs(Symbol('x'), value)

    @staticmethod
    def dividedDifference(xPoints, yPoints):
        if len(xPoints) > 2:
            xLeft = xPoints[:len(xPoints) - 1]
            xRight = xPoints[1:]
            yLeft = yPoints[:len(xPoints) - 1]
            yRight = yPoints[1:]
            return Newton.dividedDifference(xRight, yRight) - Newton.dividedDifference(xLeft, yLeft)
        if len(xPoints) == 2:
            return expand((yPoints[1] - yPoints[0]) / (xPoints[1] - xPoints[0]))
        raise IndexError(f'You are stupid? check index, dude... :-> {len(xPoints)}')

    @property
    def maxRemainder(self):
        return max([self.computeRemainder(x) for x in self.__xPoints])

    @property
    def minRemainder(self):
        return min([self.computeRemainder(x) for x in self.__xPoints])

    def __computeCentralDiffByY(self, position, pow):
        if pow == 1:
            return self.__xPoints[position + 1] - self.__xPoints[position]
        return self.__computeCentralDiffByY(position + 1, pow - 1) - self.__computeCentralDiffByY(position, pow - 1)

    def interpolate(self, xValue):

        def firstNewtonsFormula(value):
            def getPolynom(value, size):
                polynom = 1
                for j in range(size):
                    polynom *= (value - self.__xPoints[j])
                return polynom

            interpolatedValue = self.__yPoints[0]
            step = self.__xPoints[1] - self.__xPoints[0]
            for i in range(1, self.__size):
                interpolatedValue += self.__computeCentralDiffByY(0, i) / m.factorial(i) * step ** i * getPolynom(value,
                                                                                                                  i)
            return interpolatedValue

        def secondNewtonsFormula(value):
            def getPolynom(value, j, size):
                polynom = 1
                for j in range(size):
                    polynom *= (value - self.__xPoints[j])
                    j -= 1
                return polynom

            interpolatedValue = self.__yPoints[-1]
            step = self.__xPoints[1] - self.__xPoints[0]
            n = self.__size - 1
            for i in range(1, self.__size):
                interpolatedValue += self.__computeCentralDiffByY(n - 1, i) / m.factorial(i) * step ** i * getPolynom(
                    value, n, i)
                n -= 1
            return interpolatedValue

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

            def createDividedDiffTable():
                table = [[0 for _ in range(self.__size)] for _ in range(self.__size)]
                for i in range(1, self.__size):
                    for j in range(self.__size - i):
                        table[i][j] = table[j + 1][i - 1] - table[j][i - 1]
                for t, y in zip(table, self.__yPoints):
                    t[0] = y
                return table

            yTable = createDividedDiffTable()
            half = self.__size // 2
            interpolatedValue = (yTable[half - 1][0] + yTable[half][0]) / 2
            j = half - 1 if self.__size % 2 else half
            xPoint = (value - self.__xPoints[j]) / (self.__xPoints[1] - self.__xPoints[0])
            for i in range(1, self.__size):
                if i % 2:
                    interpolatedValue += (xPoint - (1 / 2) * getPolynom(xPoint, i - 1) * yTable[j][i]) / m.factorial(i)
                else:
                    interpolatedValue += (
                            getPolynom(xPoint, i) * (yTable[j][i] + yTable[j - 1][i]) / (m.factorial(i) * 2))
                    j -= 1
            return interpolatedValue

        distanceToBegin = xValue - self.__xPoints[0]
        distanceToMiddle = abs(xValue - self.__xPoints[self.__size // 2])
        distanceToEnd = self.__xPoints[-1] - xValue
        minDistance = min([distanceToBegin, distanceToMiddle, distanceToEnd])

        interpolatedValue = 0
        if minDistance == distanceToBegin:
            interpolatedValue = firstNewtonsFormula(xValue)
        elif minDistance == distanceToMiddle:
            interpolatedValue = fuckingBessel(xValue)
        elif minDistance == distanceToEnd:
            interpolatedValue = secondNewtonsFormula(xValue)
        return expand(interpolatedValue)
