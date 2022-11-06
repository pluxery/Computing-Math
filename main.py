from Lagrange import Lagrange
from Newton import *
from MathFun import MathFun as mf


_x = Symbol('x')
fun = _x ** 2 - sin(m.pi * _x)


def lab_2():
    xPoints = np.linspace(0.4, 0.9, 20)
    newton = Newton(xPoints, fun)
    testValues = [0.53, 0.43, 0.86, 0.67]
    print(f'Rn: {newton.minRemainder} < Rn(z) < {newton.maxRemainder}\n{"-" * 150}')
    for z in testValues:
        interpolatedValue = newton.interpolate(z)
        yValue = fun.subs(_x, z)
        print(f'L({z}) = {interpolatedValue}\tf(t) = {yValue}\tRn(z)= {interpolatedValue - yValue}')

    print(f'{"-" * 150}\nКонечная разность:')
    countsOfNodes = [i for i in range(2, 15, 2)]
    for n in countsOfNodes:
        _xPoints = np.linspace(0.4, 0.9, n)
        yPoints = [fun.subs(_x, val) for val in _xPoints]
        print(f'n={n}: {Newton.centralDifference(_xPoints, yPoints)}')

    print(f'{"-" * 150}')


def lab_3():
    m = 1
    n = 5
    k = 1
    _xPoints = np.linspace(0.4, 0.9, n)
    def getRemainder():
        def getPolynom():
            polynom = 1
            for i in range(len(_xPoints)):
                polynom *= (_x - _xPoints[i])
            return polynom

        return (mf.derivative(fun, n + 1) / factorial(n + 1)) * getPolynom()

    diffRemainder = mf.derivative(getRemainder(), k)

    maxRemainder = max([diffRemainder.subs(_x, x) for x in _xPoints])
    minRemainder = min([diffRemainder.subs(_x, x) for x in _xPoints])

    polynomLagrange = Lagrange(_xPoints, fun).formulaLagrange
    diffPolynomLagrange = mf.derivative(polynomLagrange, k).subs(_x, _xPoints[m])
    diffFun = mf.derivative(fun, k).subs(_x, _xPoints[m])
    remainderLagrange = diffPolynomLagrange - diffFun

    print(f'Rn : {minRemainder} < {remainderLagrange} < {maxRemainder}')


lab_2()
lab_3()
