from Lagrange import Lagrange
from Newton import *
from MathFun import MathFun as mf

_x = Symbol('x')
fun = _x ** 2 - sin(m.pi * _x)


def lab_2():
    xPoints = np.linspace(0.4, 0.9, 20)
    newton = Newton(xPoints, fun)
    testValues = [0.53, 0.43, 0.86, 0.67]
    print(f'Rn: {newton.minRemainder} < Rn(x) < {newton.maxRemainder}\n{"-" * 150}')
    for x in testValues:
        interpolatedValue = newton.interpolate(x)
        yValue = fun.subs(_x, x)
        remainder = interpolatedValue - yValue
        print('N({0}) = {1:^20}\tf({0}) = {2:^20}\tRn({0}) = {3}'.format(x, interpolatedValue, yValue, remainder))

    print(f'{"-" * 150}\nКонечная разность:')
    countsOfNodes = [i for i in range(2, 15, 2)]
    for n in countsOfNodes:
        xPoints = np.linspace(0.4, 0.9, n)
        yPoints = [fun.subs(_x, val) for val in xPoints]
        print('n = {0:^3}: {1}'.format(n, Newton.centralDifference(xPoints, yPoints)))

    print(f'{"-" * 150}')


def lab_3():
    position = 1
    countOfNodes = 5
    countOfDiff = 1
    xPoints = np.linspace(0.4, 0.9, countOfNodes)

    def getRemainder():
        def getPolynom():
            polynom = 1
            for i in range(len(xPoints)):
                polynom *= (_x - xPoints[i])
            return polynom

        return (mf.derivative(fun, countOfNodes + 1) / factorial(countOfNodes + 1)) * getPolynom()

    diffRemainder = mf.derivative(getRemainder(), countOfDiff)

    maxRemainder = max([diffRemainder.subs(_x, x) for x in xPoints])
    minRemainder = min([diffRemainder.subs(_x, x) for x in xPoints])

    polynomLagrange = Lagrange(xPoints, fun).formulaLagrange
    diffPolynomLagrange = mf.derivative(polynomLagrange, countOfDiff).subs(_x, xPoints[position])
    diffFun = mf.derivative(fun, countOfDiff).subs(_x, xPoints[position])
    remainderLagrange = diffPolynomLagrange - diffFun

    print(f'Rn : {minRemainder} < {remainderLagrange} < {maxRemainder}')


lab_2()
lab_3()
