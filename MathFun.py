import numpy as np
import math as m
from sympy import *


class MathFun:
    __x = Symbol('x')

    @classmethod
    def derivative(cls, function, countOfDiff):
        derivativeFun = function
        for _ in range(countOfDiff):
            derivativeFun = diff(derivativeFun, cls.__x)
        return derivativeFun
