import numpy as np
from Newton import *

xPoints = np.linspace(0.4, 0.9, 20)
_x = Symbol('x')
fun = _x ** 2 - sin(pi * _x)
yPoints = [fun.subs(_x, val) for val in xPoints]
N = Newton(xPoints, fun)
testValues = [0.53, 0.43, 0.86, 0.67]
print(f'Rn: {N.minRemainder} < Rn(z) < {N.maxRemainder}\n{"-" * 150}')
for z in testValues:
    interpolatedValue = N.interpolate(z)
    yValue = fun.subs(_x, z)
    print(f'L({z}) = {interpolatedValue}\tf(t) = {yValue}\tRn(z)= {interpolatedValue - yValue}')

print(f'{"-" * 150}\nКонечная разность:')
countsOfNodes = [i for i in range(2, 20, 4)]
for n in countsOfNodes:
    xPoints = np.linspace(0.4, 0.9, n)
    yPoints = [fun.subs(_x, val) for val in xPoints]
    print(f'n={n}: {Newton.dividedDifference(xPoints, yPoints)}')

print(f'{"-" * 150}')
