from Lagrange import Lagrange
from Newton import *
from MathFun import MathFun as mf

xPoints = np.linspace(0.4, 0.9, 10)
_x = Symbol('x')
fun = _x ** 2 - sin(m.pi * _x)


def lab_2(xPoints):
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
        print(f'n={n}: {Newton.centralDifference(xPoints, yPoints)}')

    print(f'{"-" * 150}')


def lab_3():
    m = 1
    n = 5
    k = 1

    def getRemainder():
        def getPolynom():
            polynom = 1
            for i in range(len(xPoints)):
                polynom *= (_x - xPoints[i])
            return polynom

        return (mf.derivative(fun, k * n + 1) / factorial(n + 1)) * getPolynom()

    diffRemainder = mf.derivative(getRemainder(), k * n)

    maxRemainder = max([diffRemainder.subs(_x, x) for x in xPoints])
    minRemainder = min([diffRemainder.subs(_x, x) for x in xPoints])

    polynomLagrange = Lagrange(xPoints, fun).formulaLagrange
    diffPolynomLagrange = mf.derivative(polynomLagrange, k * n).subs(_x, xPoints[m])
    diffFun = mf.derivative(fun, k * n).subs(_x, xPoints[m])
    remainderLagrange = diffPolynomLagrange - diffFun

    print(f'Rn : {minRemainder} < {remainderLagrange} < {maxRemainder}')


lab_2(xPoints)
lab_3()
